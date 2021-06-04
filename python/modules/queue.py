from azure.storage.queue import (QueueService, QueueMessageFormat)
import os, uuid


class MessageService:
    
    def __init__(self, connectionString):
        self.connectionString = connectionString

    def AddMessage(self, queueName, message):
        queue_service = QueueService(connection_string=self.connectionString)
        queue_service.encode_function = QueueMessageFormat.binary_base64encode
        try:
            print("Attempting to post message to Queue...")
            queue_service.put_message(queueName, message)
            print("SUCCESS: Sent message: " + message)
        except Exception as e:
            print("ERROR: Failed to put message: " + e.message)


