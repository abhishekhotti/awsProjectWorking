import json 
import test

input_file=open('/Users/ahotti/Desktop/aws/userFiles/speech.json', 'r')

json_decode=json.load(input_file)
conversation = json_decode.get('results')
oldSpeaker = ""
switchingTimes = []
endingStatement = {}
totalStatement = ""
speakerBoolean = False
punctuation = [",",".","!","?"]
for item in conversation.get("speaker_labels").get("segments"):
    if oldSpeaker != item.get("speaker_label") or oldSpeaker == "":
        oldSpeaker = item.get("speaker_label")
        switchingTimes.append(item.get("start_time"))
for item in conversation.get("items"):
    if item.get("start_time") in switchingTimes:
        endingStatement.update( {item.get("start_time"): item.get("alternatives")[0].get("content")} )
for item in conversation.get("items"):
    if item.get("start_time") in switchingTimes:
        #print("")
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
        totalStatement += wordInQ+" "
print(totalStatement)
