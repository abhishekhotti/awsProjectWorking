import boto3

from account import bucketName

BUCKET_NAME = bucketName
# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
def uploadFile2S3(filePath, saveFileAs):
    S3 = boto3.client("s3")
    S3.upload_file(filePath, BUCKET_NAME, saveFileAs, ExtraArgs={"ACL": "public-read"})
    return "https://project1-cmpe172.s3.amazonaws.com/" + saveFileAs


# SOURCE_FILENAME = '/Users/ahotti/Desktop/75485185_2431802366937167_2306894451567493120_n.jpg'
# uploadFile2S3(SOURCE_FILENAME, "test.jpg")
