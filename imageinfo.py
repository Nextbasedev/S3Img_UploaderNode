class ImageInfo:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "value": ("IMAGE", ),
                    },
                }

    FUNCTION = "imageinfo"

    CATEGORY = "imageinfo"

    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("batch", "height", "width", "channel")

    def imageinfo(self, value):
        return (value.shape[0], value.shape[1], value.shape[2], value.shape[3])


NODE_CLASS_MAPPINGS = {
    "ImageInfo": ImageInfo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageInfo": "Image Info"
}