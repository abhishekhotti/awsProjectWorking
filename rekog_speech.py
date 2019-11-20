import boto3
from account import bucketName, workingDir


def detect_text(photo, bucket):
    client = boto3.client("rekognition")
    response = client.detect_text(Image={"S3Object": {"Bucket": bucket, "Name": photo}})
    textDetections = response["TextDetections"]
    textInPic = ""
    for item in textDetections:
        if item.get("Type") == "WORD":
            textInPic += item.get("DetectedText") + " "
    return textInPic


def getSpeech(text, voiceActor):
    polly_client = boto3.client("polly")
    response = polly_client.synthesize_speech(
        VoiceId=voiceActor, OutputFormat="mp3", Text=text
    )
    file = open(workingDir + "/userFiles/speech.mp3", "wb")
    file.write(response["AudioStream"].read())
    file.close()


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
