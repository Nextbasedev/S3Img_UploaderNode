import io
import os
import torch
import base64
import random
import requests
from typing import List

from PIL import Image, ImageOps
import numpy as np

import folder_paths
import comfy.utils


MAX_RESOLUTION = 8192


def pil2tensor(image: Image.Image):
    return torch.from_numpy(pil2numpy(image)).unsqueeze(0)

def tensor2pil(image: torch.Tensor, mode=None):
    return numpy2pil(image.cpu().numpy().squeeze(), mode=mode)

def pil2numpy(image: Image.Image):
    return np.array(image).astype(np.float32) / 255.0

def numpy2pil(image: np.ndarray, mode=None):
    return Image.fromarray(np.clip(255.0 * image, 0, 255).astype(np.uint8), mode)

class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


class FlexibleOptionalInputType(dict):
    """A special class to make flexible nodes that pass data to our python handlers.

    Enables both flexible/dynamic input types (like for Any Switch) or a dynamic number of inputs
    (like for Any Switch, Context Switch, Context Merge, Power Lora Loader, etc).

    Note, for ComfyUI, all that's needed is the `__contains__` override below, which tells ComfyUI
    that our node will handle the input, regardless of what it is.

    However, with https://github.com/comfyanonymous/ComfyUI/pull/2666 a large change would occur
    requiring more details on the input itself. There, we need to return a list/tuple where the first
    item is the type. This can be a real type, or use the AnyType for additional flexibility.

    This should be forwards compatible unless more changes occur in the PR.
    """

    def __init__(self, type):
        self.type = type

    def __getitem__(self, key):
        return (self.type,)

    def __contains__(self, key):
        return True


any_type = AnyType("*")


def prepare_image_for_preview(image: Image.Image, output_dir: str, prefix=None):
    if prefix is None:
        prefix = "preview_" + "".join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))

    # save image to temp folder
    (
        outdir,
        filename,
        counter,
        subfolder,
        _,
    ) = folder_paths.get_save_image_path(prefix, output_dir, image.width, image.height)
    file = f"{filename}_{counter:05}_.png"
    image.save(os.path.join(outdir, file), format="PNG", compress_level=4)

    return {
        "filename": file,
        "subfolder": subfolder,
        "type": "temp",
    }


def load_images_from_url(urls: List[str], keep_alpha_channel=False):
    images: List[Image.Image] = []
    masks: List[Image.Image] = []

    for url in urls:
        if url.startswith("data:image/"):
            i = Image.open(io.BytesIO(base64.b64decode(url.split(",")[1])))
        elif url.startswith("file://"):
            url = url[7:]
            if not os.path.isfile(url):
                raise Exception(f"File {url} does not exist")

            i = Image.open(url)
        elif url.startswith("http://") or url.startswith("https://"):
            # Disable SSL verification for https requests
            response = requests.get(url, timeout=5, verify=False)
            if response.status_code != 200:
                raise Exception(response.text)

            i = Image.open(io.BytesIO(response.content))
        elif url.startswith(("/view?", "/api/view?")):
            from urllib.parse import parse_qs

            qs_idx = url.find("?")
            qs = parse_qs(url[qs_idx + 1 :])
            filename = qs.get("name", qs.get("filename", None))
            if filename is None:
                raise Exception(f"Invalid url: {url}")

            filename = filename[0]
            subfolder = qs.get("subfolder", None)
            if subfolder is not None:
                filename = os.path.join(subfolder[0], filename)

            dirtype = qs.get("type", ["input"])
            if dirtype[0] == "input":
                url = os.path.join(folder_paths.get_input_directory(), filename)
            elif dirtype[0] == "output":
                url = os.path.join(folder_paths.get_output_directory(), filename)
            elif dirtype[0] == "temp":
                url = os.path.join(folder_paths.get_temp_directory(), filename)
            else:
                raise Exception(f"Invalid url: {url}")

            i = Image.open(url)
        elif url == "":
            continue
        else:
            url = folder_paths.get_annotated_filepath(url)
            if not os.path.isfile(url):
                raise Exception(f"Invalid url: {url}")

            i = Image.open(url)

        i = ImageOps.exif_transpose(i)
        has_alpha = "A" in i.getbands()
        mask = None

        if "RGB" not in i.mode:
            i = i.convert("RGBA") if has_alpha else i.convert("RGB")

        if has_alpha:
            mask = i.getchannel("A")

        if not keep_alpha_channel:
            image = i.convert("RGB")
        else:
            image = i

        images.append(image)
        masks.append(mask)

    return (images, masks)


class UtilLoadImageFromUrlss:
    def __init__(self) -> None:
        self.output_dir = folder_paths.get_temp_directory()
        self.filename_prefix = "TempImageFromUrl"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "image": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False}),
                "keep_alpha_channel": (
                    "BOOLEAN",
                    {"default": False, "label_on": "enabled", "label_off": "disabled"},
                ),
                "output_mode": (
                    "BOOLEAN",
                    {"default": False, "label_on": "list", "label_off": "batch"},
                ),
                "url": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "BOOLEAN")
    OUTPUT_IS_LIST = (True, True, False)
    RETURN_NAMES = ("images", "masks", "has_image")
    CATEGORY = "Art Venture/Image"
    FUNCTION = "load_image"

    def load_image(self, image="", keep_alpha_channel=False, output_mode=False, url=""):
        if not image or image == "":
            image = url

        urls = image.strip().split("\n")
        images, masks = load_images_from_url(urls, keep_alpha_channel)
        if len(images) == 0:
            image = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu")
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            images = [tensor2pil(image)]
            masks = [tensor2pil(mask, mode="L")]

        previews = []
        np_images = []
        np_masks = []

        for image, mask in zip(images, masks):
            if mask is not None:
                preview_image = Image.new("RGB", image.size)
                preview_image.paste(image, (0, 0))
                preview_image.putalpha(mask)
            else:
                preview_image = image

            previews.append(prepare_image_for_preview(preview_image, self.output_dir, self.filename_prefix))

            image = pil2tensor(image)
            if mask:
                mask = np.array(mask).astype(np.float32) / 255.0
                mask = 1.0 - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            np_images.append(image)
            np_masks.append(mask.unsqueeze(0))

        if output_mode:
            result = (np_images, np_masks, True)
        else:
            has_size_mismatch = False
            if len(np_images) > 1:
                for image in np_images[1:]:
                    if image.shape[1] != np_images[0].shape[1] or image.shape[2] != np_images[0].shape[2]:
                        has_size_mismatch = True
                        break

            if has_size_mismatch:
                raise Exception("To output as batch, images must have the same size. Use list output mode instead.")

            result = ([torch.cat(np_images)], [torch.cat(np_masks)], True)

        return {"ui": {"images": previews}, "result": result}


NODE_CLASS_MAPPINGS = {
    "LoadImageFromUrlss": UtilLoadImageFromUrlss,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageFromUrlss": "Load Image From URLss",
    
}
