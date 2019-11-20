from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import time
import random
import string
fileNameToUse = "".join(
    random.choice(string.ascii_letters + string.digits) for i in range(12)
)
from account import workingDir, bucketName
from s3Upload import uploadFile2S3
from rekog_speech import detect_text, getSpeech, getTranslation
url = ""
app = Flask(__name__)

# fileNameToUse = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))
# workingDir = /Users/abhishekhotti/Desktop/SnapShot_Analyzer

@app.route("/")
def index():
    return redirect(url_for("chooseOne"))

@app.route("/chooseOne")
def chooseOne():
    return render_template("chooseOne.html")

@app.route("/beta")
def beta():
    return render_template("beta.html")

@app.route("/beta/translate/")
def translate():
    return render_template("translate.html")

@app.route("/beta/translateAudioDownload/")
def displayAudioBeta():
    return render_template("displayTranslateAudioBeta.html", audioFile = workingDir+"/userFiles/speech.mp3")

@app.route("/beta/translateVerify/", methods=["POST"])
def verificationStep():
    supportedVoices = {"hindi": "Aditi", "italian": "Bianca", "arabic": "Zeina", "chinese": "Zhiyu"}
    convertedText = request.form['convertedText']
    convertLang = request.form['conversionLanguage']
    getSpeech(convertedText, supportedVoices.get(convertLang))
    return redirect(url_for("displayAudioBeta"))

@app.route("/beta/convertToLanguage", methods=["POST"])
def convertToLanguage():
    supportedLanguages = {"hindi": "hi", "italian": "it", "arabic": "ar", "chinese": "zh"}
    englishText = request.form['englishText']
    convertLang = request.form['convertInto']
    translation = getTranslation(englishText, supportedLanguages.get(convertLang))
    return render_template("translatedText.html", textToTranslate = englishText, translatedText = translation, choice = convertLang)

@app.route("/pickBetaOption", methods=["POST"])
def pickBetaOption():
    choice = request.form['pickOne']
    if choice == "translate":
        return redirect(url_for("translate"))
    print(choice)
    return choice

@app.route("/pickedOption", methods=['POST'])
def pickedOption():
    fileType = request.form.get("uploadfile")
    target = os.path.join(workingDir, "userFiles/")
    actualFile = request.files.get("uploadfile")
    dest = "".join([target, actualFile.filename])
    actualFile.save(dest)
    global url
    url = uploadFile2S3(dest, "abhiTest.jpg")
    text = detect_text("abhiTest.jpg", bucketName)
    return render_template("askCorrectness.html", urlS3 = url, textToCheck = text.strip())

@app.route("/submitToSpeech", methods=['POST'])
def submitToSpeech():
    textToTranslate = request.form['correctedText']
    getSpeech(textToTranslate, "Joanna") 
    return redirect(url_for("displayAudio"))

@app.route("/downloadMP3", methods=['POST'])
def downloadMP3():
    return send_file(workingDir+"/userFiles/speech.mp3", as_attachment=True)

@app.route("/displayAudio")
def displayAudio():
    return render_template("displayAudio.html", urlS3 = url, audioFile = workingDir+"/userFiles/speech.mp3")

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
