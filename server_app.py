from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import time
import random
import string
fileNameToUse = "".join(
    random.choice(string.ascii_letters + string.digits) for i in range(12)
)

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
    choice = request.form['pickOne']
    return choice



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
