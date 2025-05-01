import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    S3_BUCKET = os.environ.get('S3_BUCKET') or 'your_bucket_name'
    S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY') or 'your_access_key'
    S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY') or 'your_secret_key'
    S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'