# import boto3
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# def upload_and_verify_image(file_path, folder_name):
#     # Get credentials and configuration from environment variables
#     bucket_name = os.getenv('S3_BUCKET_NAME')
#     access_key = os.getenv('S3_ACCESS_KEY')
#     secret_key = os.getenv('S3_SECRET_KEY')
#     region = os.getenv('S3_REGION')
#     endpoint_url = os.getenv('S3_ENDPOINT_URL')

#     # Create an S3 client
#     s3 = boto3.client('s3',
#                       aws_access_key_id=access_key,
#                       aws_secret_access_key=secret_key,
#                       region_name=region,
#                       endpoint_url=endpoint_url)
    
#     # Get the file name from the file path
#     file_name = os.path.basename(file_path)
    
#     # Specify the S3 object key (folder and file name)
#     object_key = f"{folder_name}/{file_name}"
    
#     try:
#         # Upload the file to S3
#         s3.upload_file(file_path, bucket_name, object_key)
#         print(f"Image {file_name} uploaded to {bucket_name}/{object_key}")

#         # List objects in the folder to verify upload
#         response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
#         if 'Contents' in response:
#             print(f"\nContents of {bucket_name}/{folder_name}:")
#             for obj in response['Contents']:
#                 print(f"- {obj['Key']}")
#         else:
#             print(f"\nNo objects found in {bucket_name}/{folder_name}")

#         # Generate a pre-signed URL for the uploaded image
#         url = s3.generate_presigned_url('get_object',
#                                         Params={'Bucket': bucket_name,
#                                                 'Key': object_key},
#                                         ExpiresIn=3600)  # URL expires in 1 hour
#         print(f"\nPre-signed Image URL (expires in 1 hour):\n{url}")

#         # Construct a public URL (only works if bucket and object are public)
#         public_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"
#         print(f"\nPublic Image URL (if bucket is public):\n{public_url}")

#         # If using a custom endpoint (like Backblaze B2), use this URL format
#         custom_url = f"{endpoint_url}/{bucket_name}/{object_key}"
#         print(f"\nCustom endpoint URL:\n{custom_url}")

#     except Exception as e:
#         print(f"Error: {str(e)}")

# # Example usage
# file_path = "./Screenshot_20240906_170736_Instagram.jpg"
# folder_name = "987456321"
# upload_and_verify_image(file_path, folder_name)