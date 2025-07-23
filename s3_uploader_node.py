# import os
# import boto3
# from dotenv import load_dotenv
# import numpy as np
# from PIL import Image
# import io
# import uuid
# import datetime


# class S3ImgUploaderNode:
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#         "required": {
#             "images": ("IMAGE",),
#             "folder_name1": ("STRING", {"default": "DefaultFolder1"}),
#             "folder_name2": ("STRING", {"default": "DefaultFolder2"}),
#         },
#     }

#     RETURN_TYPES = ("STRING",)
#     FUNCTION = "upload_images"
#     CATEGORY = "image"

#     def upload_images(self, images, folder_name1,folder_name2):
#         # Load environment variables
#         load_dotenv()

#         # Get S3 credentials and configuration
#         bucket_name = os.getenv('S3_BUCKET_NAME')
#         access_key = os.getenv('S3_ACCESS_KEY')
#         secret_key = os.getenv('S3_SECRET_KEY')
#         region = os.getenv('S3_REGION')
#         endpoint_url = os.getenv('S3_ENDPOINT_URL')

#         # Generate a unique folder name
   
        
#         # folder_structure = f"{current_time}_{unique_id}_ImageUpload/{folder_name}"
#         folder_structure = f"{folder_name1}/{folder_name2}"

#         # Create S3 client
#         s3 = boto3.client('s3',
#                           aws_access_key_id=access_key,
#                           aws_secret_access_key=secret_key,
#                           region_name=region,
#                           endpoint_url=endpoint_url)

#         previews = []
#         object_keys = []

#         # Check if images is a single image or a batch
#         if len(images.shape) == 3:
#             images = [images]  # Convert single image to a list
#         elif len(images.shape) == 4:
#             images = [img for img in images]  # Convert batch to list of images
#         else:
#             raise ValueError("Invalid image format")
        
#         linssss = []
#         for i, img in enumerate(images):
#             # Convert numpy array to PIL Image
#             pil_image = Image.fromarray(np.uint8(img * 255))

#             # Save image to bytes buffer
#             buffer = io.BytesIO()
#             pil_image.save(buffer, format="PNG")
#             buffer.seek(0)

#             # Generate a unique filename
#             file_name = f"image_{i}_{os.urandom(4).hex()}.png"
#             object_key = f"{folder_structure}/{file_name}"
#             link = f"https://cdn.futurebaby.ai/file/future-baby-premium/{folder_structure}/{file_name}"

#             try:
#                 # Upload to S3
#                 s3.upload_fileobj(buffer, bucket_name, object_key)
                
#                 # Generate preview URL (expires in 1 hour)
#                 # preview_url = s3.generate_presigned_url('get_object',
#                 #                                         Params={'Bucket': bucket_name,
#                 #                                                 'Key': object_key},
#                 #                                         ExpiresIn=3600)
                
#                 preview = {
#                     "type": "image",
#                     #"url": preview_url,
#                     "filename": link
#                 }
#                 previews.append(preview)
#                 object_keys.append(link)

#             except Exception as e:
#                 error_message = f"Error uploading image {i}: {str(e)}"
#                 previews.append({"type": "error", "message": error_message})
#                 object_keys.append(error_message)

#         # Create return dictionary
#         result = {
#             "ui": {"s3": previews},
#             "result": (object_keys,)
#         }

#         return result
    

# NODE_CLASS_MAPPINGS = {
#     "S3ImgUploaderNode": S3ImgUploaderNode
# }

# NODE_DISPLAY_NAME_MAPPINGS = {
#     "S3ImgUploaderNode": "S3 Image Uploader"
# }




import os
import boto3
from dotenv import load_dotenv
import numpy as np
from PIL import Image
import io
import uuid
import datetime


class S3ImgUploaderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
        "required": {
            "images": ("IMAGE",),
            "folder_name1": ("STRING", {"default": "DefaultFolder1"}),
            "folder_name2": ("STRING", {"default": "DefaultFolder2"}),
        },
    }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "upload_images"
    CATEGORY = "image"

    def upload_images(self, images, folder_name1,folder_name2):
        # Load environment variables
        load_dotenv()

        # Get S3 credentials and configuration
        bucket_name ="clotheswapper-refimg"
        access_key =  "a556292c81cb9a8d3074c75255631636"
        secret_key = "74b10d449163cf0a539b9c84b9ca0e027e9b8df1dafc16c1d378c37e389df9c3"
        region = "auto"
        endpoint_url = "https://fe1b8e17bc5bdd46e8a69af12e0b8a67.r2.cloudflarestorage.com"

        # Generate a unique folder name
   
        
        # folder_structure = f"{current_time}_{unique_id}_ImageUpload/{folder_name}"
        folder_structure = f"{folder_name1}/{folder_name2}"

        # Create S3 client
        s3 = boto3.client('s3',
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name=region,
                          endpoint_url=endpoint_url)

        previews = []
        object_keys = []

        # Check if images is a single image or a batch
        if len(images.shape) == 3:
            images = [images]  # Convert single image to a list
        elif len(images.shape) == 4:
            images = [img for img in images]  # Convert batch to list of images
        else:
            raise ValueError("Invalid image format")
        
        linssss = []
        for i, img in enumerate(images):
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(np.uint8(img * 255))

            # Save image to bytes buffer
            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")
            buffer.seek(0)

            # Generate a unique filename
            file_name = f"image_{i}_{os.urandom(4).hex()}.png"
            object_key = f"{folder_structure}/{file_name}"
            link = f"https://cdn.dressr.ai/{folder_structure}/{file_name}"

            try:
                # Upload to S3
                s3.upload_fileobj(buffer, bucket_name, object_key)
                
                # Generate preview URL (expires in 1 hour)
                # preview_url = s3.generate_presigned_url('get_object',
                #                                         Params={'Bucket': bucket_name,
                #                                                 'Key': object_key},
                #                                         ExpiresIn=3600)
                
                preview = {
                    "type": "image",
                    #"url": preview_url,
                    "filename": link
                }
                previews.append(preview)
                object_keys.append(link)

            except Exception as e:
                error_message = f"Error uploading image {i}: {str(e)}"
                previews.append({"type": "error", "message": error_message})
                object_keys.append(error_message)

        # Create return dictionary
        result = {
            "ui": {"s3": previews},
            "result": (object_keys,)
        }

        return result
    

NODE_CLASS_MAPPINGS = {
    "S3ImgUploaderNode": S3ImgUploaderNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "S3ImgUploaderNode": "S3 Image Uploader"
}
