from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import time
import random
import string
fileNameToUse = "".join(
    random.choice(string.ascii_letters + string.digits) for i in range(12)
)
from account import workingDir

totalVisitors = ""
app = Flask(__name__)

# fileNameToUse = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))
# workingDir = /Users/abhishekhotti/Desktop/SnapShot_Analyzer

@app.route("/")
def index():
    return redirect(url_for("chooseOne"))

@app.route("/chooseOne")
def chooseOne():
    return render_template("chooseOne.html")

@app.route("/pickedOption", methods=['POST'])
def pickedOption():
    fileType = request.form.get("uploadfile")
    target = os.path.join(workingDir, "userFiles/")
    actualFile = request.files.get("uploadfile")
    dest = "".join([target, actualFile.filename])
    actualFile.save(dest)
    return "done"



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
