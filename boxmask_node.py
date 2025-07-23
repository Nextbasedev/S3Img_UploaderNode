import numpy as np
import torch

def register_node():
    return BoxMaskNode()

class BoxMaskNode:
    """
    Custom ComfyUI node that takes a mask input and outputs a bounding-box mask tensor.
    The output mask has value 1.0 inside the minimal bounding rectangle enclosing
    the non-zero pixels of the input mask, and 0.0 elsewhere.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"mask": ("MASK",)}}

    RETURN_TYPES = ("MASK",)
    FUNCTION = "boxmask"
    CATEGORY = "Custom"

    def boxmask(self, mask):
        # Convert mask to numpy array
        if isinstance(mask, torch.Tensor):
            tensor = mask.detach().cpu()
            arr = tensor.numpy()
        else:
            arr = np.array(mask)

        # Squeeze singleton channel if present
        if arr.ndim == 3 and arr.shape[0] == 1:
            arr = arr.squeeze(0)

        # Collapse any extra dims into 2D
        if arr.ndim > 2:
            # Combine non-spatial dims (all but last two)
            extra_axes = tuple(range(arr.ndim - 2))
            arr = arr.any(axis=extra_axes)

        # Ensure 2D array now
        # Binary mask
        mask_bool = arr > 0
        coords = np.argwhere(mask_bool)

        # Prepare box mask
        h, w = arr.shape
        box = np.zeros((h, w), dtype=np.float32)
        if coords.size:
            y0, x0 = coords.min(axis=0)
            y1, x1 = coords.max(axis=0)
            box[y0:y1+1, x0:x1+1] = 1.0

        # Return as torch tensor (1, H, W)
        box_t = torch.from_numpy(box).unsqueeze(0)
        return (box_t,)
