from __future__ import print_function

import time
import boto3
import requests

transcribe = boto3.client('transcribe')

job_name = "translateTests"
job_uri = "https://project1-cmpe172.s3-us-west-2.amazonaws.com/trevor_trump.mp3"

transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='en-US',
    Settings = 
    {
        "ShowSpeakerLabels": True,
        "MaxSpeakerLabels": 2,
    }
    
)

def download_file(url, file_path):
    reply = requests.get(url, stream=True, verify = False)
    with open(file_path, 'wb') as file:
        for chunk in reply.iter_content(chunk_size=1024): 
            if chunk:
                file.write(chunk)

while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
urlPath = status.get('TranscriptionJob').get('Transcript').get('TranscriptFileUri')
download_file(urlPath, "/Users/ahotti/Desktop/aws/userFiles/speech.json")
transcribe.delete_transcription_job(TranscriptionJobName=job_name)
