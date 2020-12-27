import json
import os
from pathlib import Path

# Allows python to read true (json bool) to True (python bool)
true = True
false = False

contentpath = Path(__file__).parent.parent / "Content/Files"

configsfile = contentpath / "configs.txt"


def updateEvents(body_dict):
    #    newEventsDict = json.loads(body_dict)
    print("updating...")

    # Parse current config file
    with open(configsfile, "r") as f:
        #    for i, line in enumerate(f.readlines()):
        #        print(i, line)
        data = json.load(f)

    events = eval(body_dict['data'])
#    print(events)
    for event in events:
        #        print(type(event['bytes']))
        filename = contentpath / event['filename']
#        fileBytes = bytes(event['bytes'], 'utf-8')
        fileBytes = event['bytes']
#        print(fileBytes, len(fileBytes))
        # Delete file if empty bytes received
        if len(fileBytes) == 0:
            if os.path.exists(filename):
                os.remove(filename)
                print(filename, "deleted")
            event['hasPoster'] = False
        # Write poster file
        else:
            with open(filename, "wb") as f:
                f.write(bytes(fileBytes))
            print(filename, "written", len(fileBytes))
            event['hasPoster'] = True
        event.pop('bytes')

    data['events'] = events

    with open(configsfile, "w") as f:
        json.dump(data, f, indent=4)

    print("done updating events!")


def readConfigs():
    print("READING...")
    with open(configsfile, "r") as f:
        data = json.load(f)

    events = data['events']
    ticker = data['ticker']
    video = data['video']
    onTime = data['onTime']
    offTime = data['offTime']
    for event in events:
        tempfile = contentpath / event['filename']
        event['bytes'] = ''
        if os.path.exists(tempfile):
            with open(tempfile, 'rb') as f:
                tempBytes = f.read()
#                print(len(tempBytes))
                event['bytes'] = list(tempBytes)

#    print(len(events))
    tempMap = {}
    tempMap['events'] = events
    tempMap['ticker'] = ticker
    tempMap['video'] = video
    tempMap['onTime'] = onTime
    tempMap['offTime'] = offTime

#    events = json.dumps(events)
#    ticker = json.dumps(data['ticker'])

    print("done reading configs!")

    return json.dumps(tempMap)


def updateTicker(body_dict):
    print("Updating Ticker...")
    with open(configsfile, "r") as f:
        data = json.load(f)

    ticker = eval(body_dict['data'])
    data['ticker'] = ticker

    with open(configsfile, "w") as f:
        json.dump(data, f, indent=4)

    print("done updating ticker!")


def updateVideo(body_dict):
    print("Updating video link...")
    with open(configsfile, "r") as f:
        data = json.load(f)

    video = eval(body_dict['data'])
    data['video'] = video

    with open(configsfile, "w") as f:
        json.dump(data, f, indent=4)

    print("done updating video link!")
    
def updateTime(body_dict):
    print("updating on/off time...")
    with open(configsfile, "r") as f:
        data = json.load(f)

    times = eval(body_dict['data'])
    data['onTime'] = times[0]
    data['offTime'] = times[1]

    with open(configsfile, "w") as f:
        json.dump(data, f, indent=4)
    
    print("done updating on/off times!")
    
# readEvents()
