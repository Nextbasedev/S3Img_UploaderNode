from PIL import Image, ImageFile
import numpy as np
import torch
import base64
import io

# Fix for truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

class CUSTOM_OverlayTransparentImage:

    @classmethod
    def INPUT_TYPES(s):

        ALIGN_OPTIONS = [
            "center", "top left", "top center", "top right",
            "bottom left", "bottom center", "bottom right"
        ]

        return {
            "required": {
                "back_image": ("IMAGE",),
                "overlay_image_base64": ("STRING", {"default": "", "multiline": True}),
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

    def tensor2pil(self, image):
        return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

    def pil2tensor(self, image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

    def base64_to_pil(self, base64_string):
        """Convert base64 string to PIL Image"""
        try:
            # Remove data URL prefix if present
            if base64_string.startswith('data:image'):
                base64_string = base64_string.split(',')[1]

            # Fix padding if needed
            missing_padding = len(base64_string) % 4
            if missing_padding:
                base64_string += '=' * (4 - missing_padding)

            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data)).convert("RGBA")
            return image
        except Exception as e:
            raise ValueError(f"Invalid base64 image data: {str(e)}")

    def overlay_image(
        self,
        back_image,
        overlay_image_base64,
        transparency,
        offset_x,
        offset_y,
        rotation_angle,
        overlay_scale_factor=1.0,
        align='center'
    ):
        if not overlay_image_base64.strip():
            raise ValueError("Base64 image data is required")

        overlay_image = self.base64_to_pil(overlay_image_base64)

        # Adjust transparency
        r, g, b, a = overlay_image.split()
        new_alpha = a.point(lambda p: int(p * (1 - transparency)))
        overlay_image = Image.merge('RGBA', (r, g, b, new_alpha))

        # Rotate overlay image
        overlay_image = overlay_image.rotate(rotation_angle, expand=True)
        total_images = []

        for img in back_image:
            img = self.tensor2pil(img)
            background_width, background_height = img.size
            overlay_width, overlay_height = overlay_image.size

            # Maintain aspect ratio
            scale_factor_width = background_width * overlay_scale_factor / overlay_width
            scale_factor_height = background_height * overlay_scale_factor / overlay_height
            scale_factor = min(scale_factor_width, scale_factor_height)

            new_size = (
                int(overlay_width * scale_factor),
                int(overlay_height * scale_factor)
            )
            scaled_overlay = overlay_image.resize(new_size, Image.Resampling.LANCZOS)

            # Positioning
            if align == 'center':
                position_x = (background_width - scaled_overlay.width) // 2 + offset_x
                position_y = (background_height - scaled_overlay.height) // 2 + offset_y
            elif align == 'top left':
                position_x = offset_x
                position_y = offset_y
            elif align == 'top center':
                position_x = (background_width - scaled_overlay.width) // 2 + offset_x
                position_y = offset_y
            elif align == 'top right':
                position_x = background_width - scaled_overlay.width - offset_x
                position_y = offset_y
            elif align == 'bottom left':
                position_x = offset_x
                position_y = background_height - scaled_overlay.height - offset_y
            elif align == 'bottom center':
                position_x = (background_width - scaled_overlay.width) // 2 + offset_x
                position_y = background_height - scaled_overlay.height - offset_y
            elif align == 'bottom right':
                position_x = background_width - scaled_overlay.width - offset_x
                position_y = background_height - scaled_overlay.height - offset_y

            # Paste overlay
            img.paste(scaled_overlay, (position_x, position_y), scaled_overlay)
            total_images.append(self.pil2tensor(img))

        return (torch.cat(total_images, 0),)
