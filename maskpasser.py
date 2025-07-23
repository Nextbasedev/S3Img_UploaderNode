# import torch

class MaskPasser:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask1": ("MASK",),
                "mask2": ("MASK",),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "pass_mask"
    CATEGORY = "mask"

    def pass_mask(self, mask1, mask2):
        # mask1 and mask2 are torch.Tensors
        # Check if mask1 is empty (all zeros)
        if not mask1.any():
            return (mask2,)
        else:
            return (mask1,)

# Required for ComfyUI to recognize the node
NODE_CLASS_MAPPINGS = {
    "MaskPasser": MaskPasser
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskPasser": "Mask Passer (If Empty, Use Backup)"
}
