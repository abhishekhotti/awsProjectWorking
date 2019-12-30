import boto3
from account import bucketName, workingDir
import requests
import time
import json


def detect_text(photo, bucket):
    client = boto3.client("rekognition", region_name="us-west-2")
    response = client.detect_text(Image={"S3Object": {"Bucket": bucket, "Name": photo}})
    textDetections = response["TextDetections"]
    textInPic = ""
    for item in textDetections:
        if item.get("Type") == "WORD":
            textInPic += item.get("DetectedText") + " "
    return textInPic


def getSpeech(text, voiceActor, FileNameToUse):
    polly_client = boto3.client("polly", region_name="us-west-2")
    response = polly_client.synthesize_speech(
        VoiceId=voiceActor, OutputFormat="mp3", Text=text
    )
    file = open(workingDir + "/static/" + FileNameToUse + ".mp3", "wb")
    file.write(response["AudioStream"].read())
    file.close()


def download_file(url, file_path):
    reply = requests.get(url, stream=True, verify=False)
    with open(file_path, "wb") as file:
        for chunk in reply.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)


def transcribeAudioFile(s3URL, lang, peopleCount):
    transcribe = boto3.client("transcribe", region_name="us-west-2")
    job_name = "transcribeAudioFileLocal"
    job_uri = s3URL
    if peopleCount == 1:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": job_uri},
            MediaFormat="mp3",
            LanguageCode=lang,
        )
    else:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": job_uri},
            MediaFormat="mp3",
            LanguageCode=lang,
            Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": peopleCount},
        )


def downloadJson():
    transcribe = boto3.client("transcribe", region_name="us-west-2")
    job_name = "translateTestsLocal"
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status["TranscriptionJob"]["TranscriptionJobStatus"] not in [
        "COMPLETED",
        "FAILED",
    ]:
        return "failed"
    urlPath = status.get("TranscriptionJob").get("Transcript").get("TranscriptFileUri")
    download_file(urlPath, workingDir + "/userFiles/speech.json")
    transcribe.delete_transcription_job(TranscriptionJobName=job_name)

def getSingleSpeaker():
    input_file = open(workingDir + "/userFiles/speech.json", "r")
    json_decode=json.load(input_file)
    totalConvo = "Speaker 0:"
    totalConvo += json_decode.get("results").get("transcripts")[0].get("transcript")
    return totalConvo

def identifySpeakers():
    input_file = open(workingDir + "/userFiles/speech.json", "r")
    json_decode = json.load(input_file)
    conversation = json_decode.get("results")
    oldSpeaker = ""
    switchingTimes = []
    endingStatement = {}
    totalStatement = ""
    speakerBoolean = False
    punctuation = [",", ".", "!", "?"]
    for item in conversation.get("speaker_labels").get("segments"):
        if oldSpeaker != item.get("speaker_label") or oldSpeaker == "":
            oldSpeaker = item.get("speaker_label")
            switchingTimes.append(item.get("start_time"))
    for item in conversation.get("items"):
        if item.get("start_time") in switchingTimes:
            endingStatement.update(
                {item.get("start_time"): item.get("alternatives")[0].get("content")}
            )
    for item in conversation.get("items"):
        if item.get("start_time") in switchingTimes:
            totalStatement += "\n"
            if speakerBoolean is False:
                totalStatement += "Speaker 1: "
                speakerBoolean = True
            else:
                totalStatement += "Speaker 0: "
                speakerBoolean = False
        wordInQ = item.get("alternatives")[0].get("content")
        if wordInQ in punctuation:
            totalStatement = totalStatement.strip()
            totalStatement += wordInQ + " "
        else:
            totalStatement += wordInQ + " "
    return totalStatement


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
