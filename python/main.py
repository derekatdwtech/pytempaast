#!/usr/bin/env python
from modules.probe import Probe
from modules.message import Message
from modules.logger import logger
from modules.config import Config
import json
import requests
import time
import sys




# CLI Parameters
PROBE_DIR = sys.argv[1]
PROBE_NAME = sys.argv[2]
API_KEY = sys.argv[3]


# Check for command line arguments
if not PROBE_DIR or  not PROBE_NAME or not API_KEY:
    logger.error("Usage: 'python3 main.py [PROBE_DIRECTORY] [PROBE_NAME] [API_KEY]")
    quit()

#Initialize Modules
config = Config()
message = Message()
probe = Probe(PROBE_NAME, PROBE_DIR, 'w1_slave')

# Validate API_KEY. This will also return basic user Information
api_res = requests.get(config.GetApiUri() + "api/key/validate", headers=config.GetApiHeaders())
if api_res.status_code == 401:
    logger.error("Your API Key is unauthorized. Please reinitialize this service with a new API key.")
    quit()

# Set user ID from the above API Validation   
user_id = json.loads(api_res.content.decode('UTF-8'))['userId']

# Start polling
while True:
    # Check for backed messages
    message.CheckForBackUpMessages(config.GetTemperatureQueue())
    # Get Probe Configuration
    pc = probe.GetProbeConfig(user_id)
    if isinstance(pc, list):
        sleepTime = pc['readingIntervalInSeconds'][0]
    else:
        sleepTime = pc['readingIntervalInSeconds']
    logger.info("Probe read interval read as " + str(sleepTime))
    result = probe.readTemp(user_id)

    if result is not None:
       message.PostMessage(config.GetTemperatureQueue(), json.dumps(result))
    
    time.sleep(sleepTime)
    
