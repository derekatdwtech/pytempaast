import os
import glob
import time
import json
from datetime import datetime

class Probe:
    def __init__(self, name, probeDir, probeFile):
        self.name = name
        self.probeDir = probeDir
        self.probeFile = probeFile
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

    def __readTempRaw(self):
        device_folder = glob.glob(self.probeDir)[0]
        file = open(device_folder + '/' + self.probeFile, 'r')
        lines = file.readlines()
        file.close()
        return lines

    def readTemp(self):
        lines = self.__readTempRaw()
        while lines[0].strip()[-3:] != 'YES':
            print("Probe is not ready. Retrying...")
            time.sleep(1)
            lines = self.__readTempRaw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            self.temp_c = float(temp_string) / 1000.0
            self.temp_f = self.__celToFar(self.temp_c)
            
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
            result = {'name':self.name,'time':timestamp, 'id': '', 'temperature':{'f':self.temp_f,'c':self.temp_c}}
            return json.dumps(result)

    def __celToFar(self, temp_c):
        return temp_c * 9.0 / 5.0 + 32
