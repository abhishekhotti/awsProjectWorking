import boto3
from account import bucketName, workingDir
import requests
import time

def detect_text(photo, bucket):
    client = boto3.client("rekognition", region_name="us-west-2")
    response = client.detect_text(Image={"S3Object": {"Bucket": bucket, "Name": photo}})
    textDetections = response["TextDetections"]
    textInPic = ""
    for item in textDetections:
        if item.get("Type") == "WORD":
            textInPic += item.get("DetectedText") + " "
    return textInPic


def getSpeech(text, voiceActor):
    polly_client = boto3.client("polly", region_name="us-west-2")
    response = polly_client.synthesize_speech(
        VoiceId=voiceActor, OutputFormat="mp3", Text=text
    )
    file = open(workingDir + "/userFiles/speech.mp3", "wb")
    file.write(response["AudioStream"].read())
    file.close()

def download_file(url, file_path):
        reply = requests.get(url, stream=True, verify = False)
        with open(file_path, 'wb') as file:
            for chunk in reply.iter_content(chunk_size=1024): 
                if chunk:
                    file.write(chunk)

def transcribe(s3URL, lang):
    transcribe = boto3.client('transcribe', region_name="us-west-2")
    job_name = "translateTests"
    job_uri = s3URL
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode= lang
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    urlPath = status.get('TranscriptionJob').get('Transcript').get('TranscriptFileUri')
    download_file(urlPath, "/Users/ahotti/Desktop/aws/userFiles/speech.txt")
    transcribe.delete_transcription_job(TranscriptionJobName=job_name)

def getTranslation(text, countryCode):
    translate = boto3.client(
        service_name="translate", region_name="us-west-2", use_ssl=True
    )
    result = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=countryCode
    )
    return result.get("TranslatedText")


def main():
    bucket = bucketName
    photo = "abhiTest.jpg"
    textInPic = detect_text(photo, bucket)
    # print("Text detected: " + textInPic)
    # getSpeech(textInPic)


if __name__ == "__main__":
    main()
