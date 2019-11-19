import boto3
from account import bucketName

def detect_text(photo, bucket):
    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    textDetections=response['TextDetections']
    textInPic = ""
    for item in textDetections:
        if item.get("Type") == "WORD":
            textInPic += item.get("DetectedText") + " "
    return textInPic

def getSpeech(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text = text)
    file = open('/Users/ahotti/Desktop/speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

def main():
    bucket=bucketName
    photo='abhiTest.jpg'
    textInPic=detect_text(photo,bucket)
    #print("Text detected: " + textInPic)
    #getSpeech(textInPic) 


if __name__ == "__main__":
    main()