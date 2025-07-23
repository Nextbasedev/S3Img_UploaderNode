import comfy.utils
import numpy as np
import torch

class MaskRegionNode:
    def __init__(self):
        self.category = "image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "x": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "y": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "width": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "height": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "mask_region"
    INPUT_IS_LIST = True
    CATEGORY = "image"

    def mask_region(self, image, x, y, width, height):
        image = image[0]
        print(f"Image type: {type(image)}")
        print(f"Image shape: {image.shape}")
        
        # Check the length of inputs
        num_regions = len(x)
        print(f"Number of regions: {num_regions}")
        
        b, h, w, c = image.shape
        
        # Create a black background of the same size as the image
        result = torch.zeros_like(image)
        
        # Create white rectangles for each set of coordinates
        for i in range(num_regions):
            print(f"Region {i}: x={x[i]}, y={y[i]}, width={width[i]}, height={height[i]}")
            result[:, y[i]:y[i]+height[i], x[i]:x[i]+width[i], :] = 1.0  # White box
        
        print(f"Result shape: {result.shape}")
        print(f"White regions sum: {torch.sum(result)}")
        
        return (result,)

# Ensure NODE_CLASS_MAPPINGS is correctly defined
NODE_CLASS_MAPPINGS = {
    "MaskRegionNode": MaskRegionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskRegionNode": "MaskRegion Node"
}