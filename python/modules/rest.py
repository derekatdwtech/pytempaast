import requests
import json
import os
from requests.exceptions import HTTPError
import logging

class Rest:

    def __init__(self, baseUri):
        self.baseUri = baseUri
        logging.getLogger('root')

    def Get(self, route, headers):
        response = requests.get(self.baseUri + route, headers=headers)
        if(response.status_code == 200):
            return json.loads(response.content.decode('utf-8'))
        if response.status_code == 401:
            logging.exception("You are unauthorized to make this request. Your API may have expired. Please check the expiration of your API keys")
            quit()              
    
    def Post(self, route, data, headers):
        response = requests.post(self.baseUri + route, data=data, headers=headers)
        if(response.status_code == 200):
            return json.loads(response.content.decode('utf-8'))
        if response.status_code == 401:
            logging.exception("You are unauthorized to make this request. Your API may have expired. Please check the expiration of your API keys")
            quit()


