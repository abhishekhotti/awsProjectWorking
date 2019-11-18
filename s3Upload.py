import boto3

S3 = boto3.client('s3')

SOURCE_FILENAME = '/Users/ahotti/Desktop/index.txt'
BUCKET_NAME = 'project1-cmpe172'

# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, "SOURCE_FILENAME")