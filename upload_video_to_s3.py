import os
import datetime
import uuid
import logging
from botocore.exceptions import NoCredentialsError
from PIL import Image
from dotenv import load_dotenv


# Set up logger
logger = logging.getLogger(__name__)
load_dotenv()
class upload_video_to_s3:
    def __init__(self, region, access_key, secret_key, bucket_name, endpoint_url):
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.s3_client = self.get_client()

    def get_client(self):
        if not all([self.region, self.access_key, self.secret_key, self.bucket_name]):
            err = "Missing required S3 environment variables."
            logger.error(err)
            raise ValueError(err)

        try:
            import boto3
            s3 = boto3.resource(
                service_name='s3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url
            )
            return s3
        except Exception as e:
            err = f"Failed to create S3 client: {e}"
            logger.error(err)
            raise

    def upload_file(self, local_path, s3_path):
        try:
            print(f"Uploading {local_path} to {s3_path}")
            print(f"Bucket name: {self.bucket_name}")
            bucket = self.s3_client.Bucket(self.bucket_name)
            bucket.upload_file(local_path, s3_path)
            return s3_path
        except NoCredentialsError:
            err = "Credentials not available or not valid."
            logger.error(err)
            raise
        except Exception as e:
            err = f"Failed to upload file to S3: {e}"
            logger.error(err)
            raise

def get_s3_instance():
    try:
        s3_instance = upload_video_to_s3(
            bucket_name = os.getenv("S3_BUCKET_NAME") 
            access_key =  os.getenv("S3_ACCESS_KEY")
            secret_key = os.getenv("S3_SECRET_KEY")
            region = os.getenv("S3_REGION")
            endpoint_url = os.getenv("S3_ENDPOINT_URL")
        )
        return s3_instance
    except Exception as e:
        logger.error(f"Failed to create S3 instance: {e}")
        raise

S3_INSTANCE = get_s3_instance()

def resize_image_to_fit(input_path, max_size=(912, 912)):
    with Image.open(input_path) as img:
        original_width, original_height = img.size
        max_width, max_height = max_size
        scale_factor = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        new_size = (new_width, new_height)
        resized_img = img.resize(new_size, Image.LANCZOS)
        return resized_img

def save_video_files(filenames, filename_prefix="VideoFiles"):
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4()
    s3_filename = f"{current_time}_{unique_id}_{filename_prefix}"
    s3_video_paths = []
    previews = []

    base_url = "https://assets.chromastudio.ai/"

    video_file = None
    for file in filenames:
        if file.lower().endswith('.mp4') and "-audio" in file:
            video_file = file
            break
    if video_file is None:
        for file in filenames:
            if file.lower().endswith('.mp4'):
                video_file = file
                break

    if video_file:
        extension = os.path.splitext(video_file)[1].lower()
        prefix = "video/"
        s3_path = os.path.join(prefix, f"{s3_filename}{extension}")
        file_path = S3_INSTANCE.upload_file(video_file, s3_path)
        url = base_url + s3_path
        s3_video_paths.append(url)
        previews.append({
            "type": "video",
            "url": url,
            "filename": s3_path
        })

    for file in filenames:
        if file.lower().endswith('.png'):
            thumbnail_name = os.path.splitext(file)[0] + "_thumbnail.jpg"
            thumbnail_image = resize_image_to_fit(file, (912, 912))
            thumbnail_image.save(thumbnail_name, "JPEG", quality=85)

            prefix = "thumbnail/"
            s3_path = os.path.join(prefix, f"{s3_filename}.jpg")
            file_path = S3_INSTANCE.upload_file(thumbnail_name, s3_path)
            url = base_url + s3_path
            s3_video_paths.append(url)
            previews.append({
                "type": "thumbnail",
                "url": url,
                "filename": s3_path
            })

    return {"ui": {"s3": previews}, "result": s3_video_paths}
