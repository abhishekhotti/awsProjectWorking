import json 
#import test

input_file=open('/Users/abhishekhotti/Desktop/awsProjectWorking/userFiles/speech.json', 'r')

json_decode=json.load(input_file)
print(json_decode.get("results").get("transcripts")[0].get("transcript"))

#print(json_decode.get('results'))
