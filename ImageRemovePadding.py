MAX_RESOLUTION = 8192

class ImageRemovePadding:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "original_width": ("INT", { "default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1, }),
                "original_height": ("INT", { "default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1, }),
                "keep_aspect_ratio": ("BOOLEAN", { "default": True }),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT",)
    RETURN_NAMES = ("IMAGE", "width", "height",)
    FUNCTION = "execute"
    CATEGORY = "essentials/image manipulation"

    def execute(self, image, original_width, original_height, keep_aspect_ratio):
        _, current_height, current_width, _ = image.shape
        
        if keep_aspect_ratio:
            # Calculate what the proportional size would have been (same as in ImageResize pad method)
            ratio = min(current_width / original_width, current_height / original_height)
            new_width = round(original_width * ratio)
            new_height = round(original_height * ratio)
            
            # Calculate the padding that would have been added
            pad_left = (current_width - new_width) // 2
            pad_right = current_width - new_width - pad_left
            pad_top = (current_height - new_height) // 2
            pad_bottom = current_height - new_height - pad_top
            
            # Remove the padding by cropping the image
            cropped_image = image[:, pad_top:current_height-pad_bottom, pad_left:current_width-pad_right, :]
        else:
            # If not keeping aspect ratio, just return the original image (no padding to remove)
            cropped_image = image
        
        return (cropped_image, cropped_image.shape[2], cropped_image.shape[1],) 
    

# Registering node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "ImageRemovePaddings": ImageRemovePadding
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRemovePaddings": "Image Remove Paddings"
}
