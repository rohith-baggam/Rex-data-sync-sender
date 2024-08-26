from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from urllib.parse import parse_qs
from data_sync.sender_utils.websocket_utils import (
    websocket_connectivity
)
import json
from data_sync.sender_utils.utils import (
    convert_string_to_json
)
from django_data_seed.utils.colorama_theme import StdoutTextTheme


class DataSyncSenderConsumer(WebsocketConsumer, StdoutTextTheme):
    """
        This websocket does sender action
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversation_name = None

    def connect(self):
        try:
            self.accept()
            self.conversation_name = "data_sync"
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_name,
                self.channel_name
            )

        except Exception as e:
            self.close(code=f"something went wrong in conncet, {str(e)}")
            print(f"Connection error: {e}")

    def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                text_data_json = convert_string_to_json(text_data)

                if not isinstance(text_data_json, dict):
                    self.close(code=f"Incorrect format, {str(e)}")
                    return

                websocket_connectivity(text_json=text_data_json)
        except Exception as e:
            self.close(code=f"something went wrong in recieve, {str(e)}")
            print(f"Receive error: {e}")

    def disconnect(self, close_code=None):
        return

    def sender_layer(self, event):
        self.send(text_data=json.dumps(event))

    def token_verification(self, event):
        self.send(text_data=json.dumps(event))

    def secret_key_verification(self, event):
        self.send(text_data=json.dumps(event))

    def schema_verification(self, event):
        self.send(text_data=json.dumps(event))

    def data_transformation(self, event):
        self.send(text_data=json.dumps(event))

    def data_information(self, event):
        self.send(text_data=json.dumps(event))

    def data_transformation_successful(self, event):
        self.send(text_data=json.dumps(event))
