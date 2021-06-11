from modules.probe import Probe
from modules.queue import MessageService
from modules.rest import Rest
import time
import os
import json
import glob
import sys
import logging

# CLI Parameters
PROBE_DIR = sys.argv[1]
PROBE_NAME = sys.argv[2]
API_KEY = sys.argv[3]
API_URI="https://meatmonitor.azurewebsites.net/"

#Variables to hold values
headers={'Api-Key', API_KEY}

#Initialize Logger
logging.basicConfig(filename='pytempaast.log', filemode='a')

if not PROBE_DIR or PROBE_NAME or API_KEY:
    logging.error("Usage: 'python3 main.py [PROBE_DIRECTORY] [PROBE_NAME] [API_KEY]")

#Initialize REST Module
rest =  Rest(API_URI)

# Validate API_KEY. This will also return basic user Information
logging.info("Validating API Key...")
user_id = rest.Get("api/key/validate", headers)

# Get or Create Probe Configuration
logging.info("Attempting to get probe config from the API")

probeConfig = rest.Get("api/probe/config/" + PROBE_NAME, headers)
if probeConfig == "":
    logging.info("No configuration for this device was found. Creating with base configuration...")
    PROBE_ID=PROBE_DIR.split("/")
    BASE_CONFIG={"partitionKey": user_id, "rowKey": PROBE_ID[len(PROBE_ID) - 1], "nickname": PROBE_NAME, "readingIntervalInSeconds": 300, "tempThresholdInCelcius": 0, "user_id": user_id}
    probeConfig = rest.Post("api/probe/config", BASE_CONFIG, headers)
    
probe = Probe(PROBE_NAME, PROBE_DIR, 'w1_slave')

while True:
    sleepTime = probeConfig['readingIntervalInSeconds']
    logging.info("Probe interval read as " + str(sleepTime))
    result = probe.readTemp()
    rest.Post("api/message?temperature", result, headers)
    time.sleep(sleepTime)
    
