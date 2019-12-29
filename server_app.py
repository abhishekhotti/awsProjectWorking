
from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import time
import random
import string

fileNameToUse = ""
from account import workingDir, bucketName
from s3Upload import uploadFile2S3
from awsFunctions import detect_text, getSpeech, getTranslation, transcribeAudioFile, identifySpeakers, downloadJson

url = ""
totalConvo = ""
app = Flask(__name__)

# fileNameToUse = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))
# workingDir = /Users/abhishekhotti/Desktop/SnapShot_Analyzer


@app.route("/")
def index():
    for subdir, dirs, files in os.walk(workingDir+"/static/"):
        for file in files:
            if file.endswith(".mp3"):
                os.remove(workingDir+"/static/"+file)
    for subdir, dirs, files in os.walk(workingDir+"/userFiles/"):
        for file in files:
            os.remove(workingDir+"/userFiles/"+file)
    global fileNameToUse
    fileNameToUse = "".join(random.choice(string.ascii_letters + string.digits) for i in range(12))
    return redirect(url_for("chooseOne"))


@app.route("/chooseOne")
def chooseOne():
    return render_template("chooseOne.html")


@app.route("/beta/")
def beta():
    for subdir, dirs, files in os.walk(workingDir+"/static/"):
        for file in files:
            if file.endswith(".mp3"):
                os.remove(workingDir+"/static/"+file)
    for subdir, dirs, files in os.walk(workingDir+"/userFiles/"):
        for file in files:
            os.remove(workingDir+"/userFiles/"+file)
    global fileNameToUse
    fileNameToUse = "".join(random.choice(string.ascii_letters + string.digits) for i in range(12))
    return render_template("beta.html")


@app.route("/beta/translate/")
def translate():
    return render_template("translate.html")

@app.route("/beta/transcribe/")
def transcribe():
    return render_template("transcribe.html")


@app.route("/beta/translateAudioDownload/")
def displayAudioBeta():
    print("here")
    return render_template(
        "displayTranslateAudioBeta.html", audioFile=fileNameToUse+".mp3"
    )


@app.route("/beta/translateVerify/", methods=["POST"])
def verificationStep():
    supportedVoices = {
        "hindi": "Aditi",
        "italian": "Bianca",
        "arabic": "Zeina",
        "chinese": "Zhiyu",
        "danish": "Naja",
        "dutch": "Lotte",
        "french": "Mathieu",
        "german": "Marlene",
        "spanish": "Lupe"
    }
    convertedText = request.form["convertedText"]
    convertLang = request.form["conversionLanguage"]
    getSpeech(convertedText, supportedVoices.get(convertLang), fileNameToUse)
    return redirect(url_for("displayAudioBeta"))

@app.route("/beta/downloadTranscript", methods=["POST"])
def downloadTranscript():
    text = request.form["correctedText"]
    print(text)
    return send_file(workingDir+"/userFiles/downTranscript.txt", as_attachment=True)

@app.route("/beta/checkForJsonFile", methods=["POST"])
def checkForJsonFile():
    jsonFile = request.form['fileName']
    if "failed" == downloadJson():
        return redirect(url_for("doingMagic"))
    for subdir, dirs, files in os.walk(workingDir+"/userFiles/"):
        for file in files:
            if file == "speech.json":
                global totalConvo
                totalConvo = identifySpeakers()
                with open(workingDir+"/userFiles/downTranscript.txt", "w+") as writeFile:
                    writeFile.write(totalConvo)
                return redirect(url_for("displayTranscript"))
    

@app.route("/beta/transcribeAudio", methods=["POST"])
def transcribeAudio():
    fileType = request.form.get("uploadfile")
    userCount = request.form["peopleCount"]
    target = os.path.join(workingDir, "userFiles/")
    actualFile = request.files.get("uploadfile")
    dest = "".join([target, actualFile.filename])
    actualFile.save(dest)
    fsize=os.stat(dest)
    if fsize.st_size > 5000000:
        return render_template("transcribe.html", fail = "Upload only a file less than 5 MB")
    global url 
    return "done"
    url = uploadFile2S3(dest, "abhiTest.mp3")
    transcribeAudioFile(url, "en-US", int(userCount))
    return redirect(url_for("doingMagic"))
    

@app.route("/beta/doingMagic")
def doingMagic():
    return render_template("loadingPage.html", fileNameToUse = "speech.json")

@app.route("/beta/transcript")
def displayTranscript():
    global totalConvo
    totalConvo = totalConvo.split("\n")
    for index, value in enumerate(totalConvo):
        totalConvo[index] = value.split(":")
    return render_template("displayTranscript.html", speakerNotes = totalConvo, totalCount = len(totalConvo), transcript= workingDir+"/userFiles/downTranscript.txt")

@app.route("/beta/convertToLanguage", methods=["POST"])
def convertToLanguage():
    supportedLanguages = {
        "hindi": "hi",
        "italian": "it",
        "arabic": "ar",
        "chinese": "zh",
        "danish": "da",
        "dutch": "nl",
        "french": "fr",
        "german": "de",
        "spanish": "es",
    }
    englishText = request.form["englishText"]
    convertLang = request.form["convertInto"]
    translation = getTranslation(englishText, supportedLanguages.get(convertLang))
    return render_template(
        "translatedText.html",
        textToTranslate=englishText,
        translatedText=translation,
        choice=convertLang,
    )


@app.route("/pickBetaOption", methods=["POST"])
def pickBetaOption():
    choice = request.form["pickOne"]
    if choice == "translate":
        return redirect(url_for("translate"))
    elif choice == "transcribe":
        return redirect(url_for("transcribe"))
    return choice


@app.route("/pickedOption", methods=["POST"])
def pickedOption():
    target = os.path.join(workingDir, "userFiles/")
    actualFile = request.files.get("uploadfile")
    dest = "".join([target, actualFile.filename])
    actualFile.save(dest)
    fsize=os.stat(dest)
    if fsize.st_size > 5000000:
        return render_template("chooseOne.html", fail = "Upload only a file less than 5 MB")
    global url
    url = uploadFile2S3(dest, "abhiTest.jpg")
    text = detect_text("abhiTest.jpg", bucketName)
    return render_template("askCorrectness.html", urlS3=url, textToCheck=text.strip())


@app.route("/submitToSpeech", methods=["POST"])
def submitToSpeech():
    textToTranslate = request.form["correctedText"]
    global url
    url = request.form['s3URL']
    getSpeech(textToTranslate, "Joanna", fileNameToUse)
    return redirect(url_for("displayAudio"))


@app.route("/downloadMP3", methods=["POST"])
def downloadMP3():
    return send_file(workingDir + "/static/"+fileNameToUse+".mp3", as_attachment=True)


@app.route("/displayAudio")
def displayAudio():
    return render_template(
        "displayAudio.html", urlS3=url, audioFile=fileNameToUse+".mp3"
    )

@app.errorhandler(404)
def error404(error):
    return render_template("error404.html")

@app.errorhandler(500)
def error500(error):
    return render_template("reportError.html")


@app.errorhandler(405)
def error405(error):
    return render_template("error404.html")

if __name__ == "__main__":
    app.run(debug=True)
