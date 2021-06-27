import os
import glob
import time
import json
import logging
import requests
from modules.config import Config
from modules.logger import logger
from datetime import datetime



class Probe:
    def __init__(self, name, probeDir, probeFile):
        self.name = name
        self.probeDir = probeDir
        self.probeFile = probeFile
        self.probeConfig = {}
        self.config = Config()

        if not os.path.exists(self.probeDir + "/" + self.probeFile):
            logger.critical("File not found at " + self.probeDir + "/" + self.probeFile + ". Please ensure your probe is working correctly and restart the service.")
            quit()

        if os.system('modprobe w1-gpio') != 0 and os.system('modprobe w1-therm') != 0:
            logger.critical("'modprobe' failed to execute. Ensure the modprobe executable exists on your system.")
            #quit()

    # Read Raw Temperature
    def __readTempRaw(self):
        device_folder = glob.glob(self.probeDir)[0]
        file = open(device_folder + '/' + self.probeFile, 'r')
        lines = file.readlines()
        file.close()
        return lines

    # Convert temp
    def __celToFar(self, temp_c):
        return temp_c * 9.0 / 5.0 + 32

    def readTemp(self, user):
        PROBE_ID_TEMP=self.probeDir.split("/")
        PROBE_ID=PROBE_ID_TEMP[len(PROBE_ID_TEMP) - 1]
        lines = self.__readTempRaw()
        while lines[0].strip()[-3:] != 'YES':
            logger.info("Probe is not ready. Retrying in 5 seconds...")
            time.sleep(5)
            lines = self.__readTempRaw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            self.temp_c = float(temp_string) / 1000.0
            self.temp_f = self.__celToFar(self.temp_c)

            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z")
            result = {'nickname':self.name,'time':timestamp, 'probe_id': PROBE_ID , 'user_id': user, 'temperature':{'f':self.temp_f,'c':self.temp_c}}
            return json.dumps(result)

    def GetProbeConfig(self, user):
        PROBE_ID_TEMP = self.probeDir.split("/")
        PROBE_ID = PROBE_ID_TEMP[len(PROBE_ID_TEMP) - 1]
        BASE_CONFIG={"partitionKey": user, "rowKey": PROBE_ID, "nickname": self.name, "readingIntervalInSeconds": 300, "tempThresholdInCelcius": 0, "user_id": user}

        res = requests.get(self.config.GetApiUri() + "api/probe/config?probeId=" + PROBE_ID, headers=self.config.GetApiHeaders())
        if res.ok:
            result = json.loads(res.content.decode('utf-8'))
            self.probeConfig = result
        elif res.status_code == 404:
            logger.warn("No probe configuration was found for probe " + PROBE_ID + ". Creating new configuration with config base...")
            conf = requests.post(self.config.GetApiUri() + "api/probe/config", headers=self.config.GetApiHeaders(), data=json.dumps(BASE_CONFIG))
            if conf.status_code == 200:
                result = []
                result.append(json.loads(conf.content.decode("UTF-8")))
                self.probeConfig = result
            else:
                logger.error("Unable to create new probe configuration. Using default configuration.")
                self.probeConfig = json.loads([BASE_CONFIG])
        else:
            logger.error("An unknown error has occurred trying to retrieve probe configuration. Response code: " + str(res.status_code) + ". Message: " + res.text + ". Falling back to previously used configuration.")
            if not self.probeConfig:
                logger.critical("PANIC: If we have reached this far without a probe configuration, something has gone terribly wrong. Please contact the developers.")    