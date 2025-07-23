from dotenv import load_dotenv
import os
import boto3

load_dotenv()

# Get S3 credentials and configuration
bucket_name = os.getenv('S3_BUCKET_NAME')
access_key = os.getenv('S3_ACCESS_KEY')
secret_key = os.getenv('S3_SECRET_KEY')
region = os.getenv('S3_REGION')
endpoint_url = os.getenv('S3_ENDPOINT_URL')


print(bucket_name,access_key,secret_key,region,endpoint_url)


# Create an S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region,
    endpoint_url=endpoint_url  # Optional, if you are using a custom endpoint
)

def upload_image(file_name, bucket, object_name=None):
    """
    Uploads an image to an S3 bucket.

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
        return True
    except Exception as e:
        print(f"Failed to upload {file_name} to {bucket}/{object_name}: {e}")
        return False

# Example usage
file_name = './as.jpg'
upload_image(file_name, bucket_name)