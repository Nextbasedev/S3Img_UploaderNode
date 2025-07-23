from PIL import Image
import numpy as np
import torch
import os


class CUSTOM_OverlayTransparentImage:

    @classmethod
    def INPUT_TYPES(s):

        ALIGN_OPTIONS = ["center", "top left", "top center", "top right", "bottom left", "bottom center", "bottom right"]

        return {"required": {
            "back_image": ("IMAGE",),
            "overlay_image": ("STRING", {"default": "VideoFiles"}),
            "align": (ALIGN_OPTIONS,),
            "transparency": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.1}),
            "offset_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "offset_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
            "overlay_scale_factor": ("FLOAT", {"default": 1.000, "min": 0.000, "max": 100.000, "step": 0.001}),
        }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "overlay_image"
    CATEGORY = "ComfyS3"

    def tensor2pil(self,image):
        return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

    def pil2tensor(self,image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

    def overlay_image(self, back_image, overlay_image,
                      transparency, offset_x, offset_y, rotation_angle, overlay_scale_factor=1.0, align='center'):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-overlay-transparent-image"

        # Create PIL images for the text and background layers and text mask
        overlay_image_path = os.path.join(os.path.dirname(__file__), overlay_image)
        overlay_image = Image.open(overlay_image_path).convert("RGBA")

        # Split the overlay image into its individual channels
        r, g, b, a = overlay_image.split()

        # Create a new alpha channel with adjusted transparency
        new_alpha = a.point(lambda p: int(p * (1 - transparency)))

        # Merge the channels back together
        overlay_image = Image.merge('RGBA', (r, g, b, new_alpha))

        # Rotate overlay image
        overlay_image = overlay_image.rotate(rotation_angle, expand=True)
        total_images = []

        for img in back_image:
            img = self.tensor2pil(img)

            # Scale overlay image based on background image size
            background_width, background_height = img.size
            overlay_width, overlay_height = overlay_image.size

            # Calculate scale factors based on the background image dimensions
            scale_factor_width = background_width * overlay_scale_factor / overlay_width
            scale_factor_height = background_height * overlay_scale_factor / overlay_height

            # Use the smaller scale factor to maintain aspect ratio
            scale_factor = min(scale_factor_width, scale_factor_height)
            new_size = (int(overlay_width * scale_factor), int(overlay_height * scale_factor))
            overlay_image = overlay_image.resize(new_size, Image.Resampling.LANCZOS)

            # Calculate position based on alignment
            if align == 'center':
                position_x = (background_width - overlay_image.width) // 2 + offset_x
                position_y = (background_height - overlay_image.height) // 2 + offset_y
            elif align == 'top left':
                position_x = offset_x
                position_y = offset_y
            elif align == 'top center':
                position_x = (background_width - overlay_image.width) // 2 + offset_x
                position_y = offset_y
            elif align == 'top right':
                position_x = background_width - overlay_image.width - offset_x
                position_y = offset_y
            elif align == 'bottom left':
                position_x = offset_x
                position_y = background_height - overlay_image.height - offset_y
            elif align == 'bottom center':
                position_x = (background_width - overlay_image.width) // 2 + offset_x
                position_y = background_height - overlay_image.height - offset_y
            elif align == 'bottom right':
                position_x = background_width - overlay_image.width - offset_x
                position_y = background_height - overlay_image.height - offset_y

            # Paste the rotated overlay image onto the new back image at the specified position
            img.paste(overlay_image, (position_x, position_y), overlay_image)

            total_images.append(self.pil2tensor(img))

        images_out = torch.cat(total_images, 0)

        # Convert the PIL image back to a torch tensor
        return (images_out,)