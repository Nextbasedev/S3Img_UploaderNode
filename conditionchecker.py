import torch
import comfy.utils

class StringConditionalNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "condition": ("STRING", {"default": "True"}),
                "image": ("IMAGE",),
                "mask": ("MASK",),
            },
        }
    
    RETURN_TYPES = ("MASK", "IMAGE")
    FUNCTION = "route_output"
    CATEGORY = "flow control"

    def route_output(self, condition, image, mask):
        if isinstance(condition, str):
            condition = condition.lower() == "true"
        elif not isinstance(condition, bool):
            raise ValueError("Input must be a string ('True' or 'False') or a boolean")

        if condition:
            return (mask, image)
        else:
            return (None, image)

NODE_CLASS_MAPPINGS = {
    "StringConditionalNode": StringConditionalNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringConditionalNode": "String Conditional"
}


