import boto3
S3_BUCKET_NAME="future-baby-public"
S3_ACCESS_KEY="00556192c8fcb810000000001"
S3_SECRET_KEY="K005Xeq0a0RN1T/WlkomPPKgKr+HybU"
S3_REGION="us-east-005"
S3_ENDPOINT_URL="https://s3.us-east-005.backblazeb2.com/"

# # Replace with your Backblaze S3 credentials
# B2_ACCESS_KEY = "your-access-key"
# B2_SECRET_KEY = "your-secret-key"
# B2_BUCKET_NAME = "your-bucket-name"
# B2_ENDPOINT = "https://s3.us-west-002.backblazeb2.com"  # Change region if needed

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

# Function to upload an image
def upload_image(image_path, key):
    try:
        s3_client.upload_file(image_path, S3_BUCKET_NAME, key, ExtraArgs={'ContentType': 'image/jpeg'})
        print(f"Image '{image_path}' uploaded as '{key}'")
    except Exception as e:
        print(f"Upload error: {e}")

# Example usage
if __name__ == "__main__":
    upload_image("Screenshot_20240906_170736_Instagram.jpg", "uploads/example.jpg")  # Upload an image to 'uploads/' folder
