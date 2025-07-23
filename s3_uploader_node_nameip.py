import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import numpy as np

from PIL import Image
import io

class S3ImgUploaderNodeImageNamePrefix:
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
        load_dotenv()
        bucket_name = os.getenv('S3_BUCKET_NAME')
        access_key = os.getenv('S3_ACCESS_KEY')
        secret_key = os.getenv('S3_SECRET_KEY')
        region = os.getenv('S3_REGION')

        endpoint_url = os.getenv('S3_ENDPOINT_URL')
        
        folder_structure = f"{folder_name1}/{folder_name2}"
        s3 = boto3.client('s3',
                          endpoint_url=endpoint_url,
                          region_name=region,
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          )

        previews = []
        object_keys = []

        if len(images.shape) == 3:
            images = [images]
        elif len(images.shape) == 4:
            images = [img for img in images]
        else:
            raise ValueError("Invalid image format")

        for i, img in enumerate(images):
            pil_image = Image.fromarray(np.uint8(img * 255))
            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")
            buffer.seek(0)

            file_name = f"{file_name_prefix}_{i}.png"
            object_key = f"{folder_structure}/{file_name}"

            try:
                s3.upload_fileobj(buffer, bucket_name, object_key, ExtraArgs={'ContentType': 'image/png'})
                public_url = f"https://cdn.smartshot.ai/{object_key}"
                previews.append({"type": "image", "filename": public_url})
                object_keys.append(public_url)

            except ClientError as e:
                error_message = f"Error uploading image {i}: {str(e)}"
                previews.append({"type": "error", "message": error_message})
                object_keys.append(error_message)

        result = {
            "ui": {"s3": previews},
            "result": (object_keys,)
        }

        return result

NODE_CLASS_MAPPINGS = {
    "S3ImgUploaderNode": S3ImgUploaderNodeImageNamePrefix
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "S3ImgUploaderNode": "S3 Image Uploader"
}