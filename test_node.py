# import boto3
import os
# from botocore.exceptions import ClientError
# from dotenv import load_dotenv
import numpy as np

# from PIL import Image
# import io

class test_node:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "folder_name1": ("STRING", {"default": "DefaultFolder1"}),
                "folder_name2": ("STRING", {"default": "DefaultFolder2"}),
                "file_name_prefix": ("STRING", {"default": "image"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "upload_images"
    CATEGORY = "image"

    def upload_images(self, images, folder_name1, folder_name2, file_name_prefix):
        print("upload_imagesdasasasasasasasasasasasasasasasasasasasas")
        return "test"

        return result

NODE_CLASS_MAPPINGS = {
    "test_node": test_node
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "test_node": "test_node"
}