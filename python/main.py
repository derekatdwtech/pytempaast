from modules.probe import Probe
from modules.queue import MessageService
from modules.config import Config
import time
import os
import json
import glob
import sys

data = ""
connString = ""
probeName = ""
try:
    print("Loading configuration file")
    with open("/opt/meatmonitor/config.json") as file:
        data = json.load(file)
        connString = "DefaultEndpointsProtocol=https;AccountName=" + data['storageAccountName'] + ";AccountKey=" + data['storageAccountKey'] + ";EndpointSuffix=core.windows.net"
        #probeName = data["probeName"]
except Exception as e:
    print("Failed to load configuration file. Exiting Application with error: "+ e.message)
    quit()

# Get Probe Identifier
deviceDirectories = os.listdir('/sys/bus/w1/devices')
if len(deviceDirectories) > 0:
    for device in deviceDirectories:
        if device.startswith('28-'):
            probeName=str(device)
    if probeName == "":
        sys.exit("ERROR: No probes have been found. Exiting Application")
            



queue = MessageService(connString)
probe = Probe(probeName, '/sys/bus/w1/devices/' + probeName, 'w1_slave')
print("Initializing Probe Configuration")

probeConfig = Config(data['apiBaseUri'])
while True:
    sleepTime = probeConfig.GetConfig('probe/config/' + probeName)
    print("Probe interval read as " + str(sleepTime['readingIntervalInSeconds']))
    result = probe.readTemp()
    queue.AddMessage(data['storageQueueName'], result)
    time.sleep(sleepTime['readingIntervalInSeconds'])
    
