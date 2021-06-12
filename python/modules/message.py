from modules.config import Config
from modules.logger import logger
from os.path import exists
import requests



class Message:
    def __init__(self):
        self.config = Config()

    def PostMessage(self, queue, data):
        res = requests.post(self.config.GetApiUri() + "api/message?queue=" + queue, data=data, headers=self.config.GetApiHeaders())
        if res.status_code != 200:
            logger.error("We were unable to send your message. We will save it locally and send it later. Status code: " + str(res.status_code) + " Error: " + res.text)
            with open("backup_readings.bak", mode='a') as readings:
                readings.write(data + "\n")
            readings.close()
            return False
        else: 
            logger.debug("Successfully sent message " + data)
            logger.info("Successfully sent temperature reading")
            return True

    def CheckForBackUpMessages(self, queue):
        if exists('backup_readings.bak'):
            logger.info("We have found failed messages. Attempting to resend them.")
            with open('backup_readings.bak', 'r') as file:
                lines = file.readlines()
            
            with open('backup_readings.bak', 'w') as out:
                for line in lines:
                    res = requests.post(self.config.GetApiUri() + "api/message?queue=" + queue, data=line, headers=self.config.GetApiHeaders())
                    if res != 200:
                        out.write(line)
            out.close()
            file.close()




                    

