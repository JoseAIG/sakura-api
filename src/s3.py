import os
import boto3

s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def uploadFile(directory: str, filename: str):
    fileKey = directory + filename
    s3.upload_file(filename, BUCKET_NAME, fileKey, ExtraArgs={'ACL':'public-read'})
    return "https://{0}.s3.amazonaws.com/{1}".format(BUCKET_NAME, fileKey)