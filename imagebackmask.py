import torch
import numpy as np
from PIL import Image

class ImageBackMask:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "background": ("IMAGE",),
                "object": ("IMAGE",),
                "left": ("INT", {"default": 0, "min": -10000, "max": 10000}),
                "top": ("INT", {"default": 0, "min": -10000, "max": 10000}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "combine_images"
    CATEGORY = "image/processing"

    def combine_images(self, background, object, left, top, scale):
        # Ensure background and object are 3D tensors (B, H, W, C)
        background = background.squeeze(0) if background.dim() == 4 else background
        object = object.squeeze(0) if object.dim() == 4 else object

        # Convert tensors to PIL Images
        background_pil = Image.fromarray((background * 255).byte().cpu().numpy())
        object_pil = Image.fromarray((object * 255).byte().cpu().numpy(), mode='RGBA')

        # Scale the object image
        new_size = (int(object_pil.width * scale), int(object_pil.height * scale))
        object_pil = object_pil.resize(new_size, Image.LANCZOS)

        # Create a new image with the same size as the background
        result = background_pil.copy()

        # Calculate center position
        center_left = (background_pil.width - object_pil.width) // 2
        center_top = (background_pil.height - object_pil.height) // 2

        # Calculate paste position, scaling the offset by the scale factor
        # Note the change here for left: we add instead of subtract
        paste_left = center_left + int(left * scale)
        paste_top = center_top - int(top * scale)

        # Ensure the object fits within the background
        paste_left = max(0, min(paste_left, background_pil.width - object_pil.width))
        paste_top = max(0, min(paste_top, background_pil.height - object_pil.height))

        # Paste the object onto the background
        result.paste(object_pil, (paste_left, paste_top), object_pil)

        # Convert back to tensor
        result_tensor = torch.from_numpy(np.array(result).astype(np.float32) / 255.0)
        
        # Ensure the tensor has the correct shape (B, H, W, C)
        result_tensor = result_tensor.unsqueeze(0)

        return (result_tensor,)

NODE_CLASS_MAPPINGS = {
    "ImageBackMask": ImageBackMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageBackMask": "Image Back Mask",
}
