import torch
from torch import Tensor

class MaskBatchCombiner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "process"
    CATEGORY = "image"

    def process(self, images: Tensor):
        if len(images.shape) == 4:  # [batch, height, width, channels]

            batch_size = images.shape[0]
            if batch_size > 1:
                return (images, "batch")
            else:
                return (images.squeeze(0), "single")
        elif len(images.shape) == 3:  # [height, width, channels]
            return (images.unsqueeze(0), "single")
        else:
            raise ValueError(f"Unexpected image shape: {images.shape}")

NODE_CLASS_MAPPINGS = {
    "MaskBatchCombiner": MaskBatchCombiner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskBatchCombiner": "Mask Batch Combiner"
}
