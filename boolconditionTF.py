import torch
import comfy.utils

class BoolConditionTF:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "condition": ("STRING", {"default": "True"})
            }
        }
    
    RETURN_TYPES = ("INT", "INT")
    FUNCTION = "process"
    CATEGORY = "utils"

    def process(self, condition):
        print("condition ----------------------",condition)
        # condition = condition.lower().strip()
        if condition == True:
            return (0, 1)
        elif condition == False:
            return (1, 0)
        else:
            raise ValueError("Input must be 'True' or 'False'")

NODE_CLASS_MAPPINGS = {
    "BoolConditionTF": BoolConditionTF
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BoolConditionTF": "Boolean Condition (True/False)"
}

