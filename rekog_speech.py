import boto3
from account import bucketName

def detect_text(photo, bucket):
    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    textDetections=response['TextDetections']
    return textDetections[0]['DetectedText']

def getSpeech(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text = text)
    file = open('/Users/ahotti/Desktop/speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

def main():
    bucket=bucketName
    photo='75485185_2431802366937167_2306894451567493120_n.jpg'
    textInPic=detect_text(photo,bucket)
    print("Text detected: " + textInPic)
    getSpeech(textInPic) 



if __name__ == "__main__":
    main()