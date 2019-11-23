# awsProjectWorking
University Name: http://www.sjsu.edu/ (Links to an external site.)

Course: Enterprise Software (Links to an external site.)

Professor Sanjay Garje (Links to an external site.) (This is link to LinkedIn Profile)

Student: 
1) Abhishek Hotti (https://www.linkedin.com/in/abhishek-hotti/)
2) Moo Jin Park (https://www.linkedin.com/in/moopark03/)

Application:
1) Recognize text in an image
2) Read out text from image
3) Allow user to login
4) Can translate text into another language
5) Transcribe an audio recording (meeting recordings)
6) Read out translated statements in different languages

Bare Minimum Pre Reqs:
1) EC2
2) S3
3) Rekognition
4) Polly
5) Transcribe

Extra:
1) Transcribe
2) Translate

Local Software:
1) Python3 (Python2 is being phased out)
2) Flask
3) Boto3
4) Virtual Environment (recommended)
5) Create a file called "account.py" and make it have these lines: 
     import os
     bucketName = '--bucketNameHere--'
     workingDir = os.getcwd()

Commands to run locally:
1) Open terminal
2) Navigate into folder where the python file (server_app.py) is located
3) Type in: (sudo) python3 server_app.py
4) Open web browser and head to http://127.0.0.1:5000/

