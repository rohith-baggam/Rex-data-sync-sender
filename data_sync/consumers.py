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


class DataSyncSenderConsumer(WebsocketConsumer):

    """
        This web socket does sender action
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.conversation_name = None

    def connect(self):
        try:
            self.accept()
            query_string_bytes = self.scope.get("query_string", b"")
            query_string = parse_qs(query_string_bytes.decode("utf-8"))
            token_info = query_string["token"][0]
            print('token_info', token_info)
            if token_info == False:
                self.disconnect("UNAUTHORIZED")
            self.conversation_name = "data_sync"
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_name,
                self.channel_name,
            )
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "sender_layer",
                    "conversations": self.conversation_name,
                    "data": {
                        "status_code": 200,
                        "message": "Connected",
                        "buffer_data": None
                    }
                },
            )
        except Exception as e:

            self.disconnect(
                close_code=f"Receiver was disconnected due to , {str(e)}")

    def receive(self, text_data=None, bytes_data=None):
        try:
            try:
                print('text_data', text_data, type(text_data))
                text_data_json = convert_string_to_json(text_data)
                # text_data_json = text_data
                print(0)
                # text_data_json = json.loads(text_data)
                # text_data_json = json.dumps(text_data_json)
            except Exception as e:
                print('Exception', e)
                text_data_json = {}
                self.disconnect(
                    f'json convertion error, {str(e)}'
                )
                return
            print(1, text_data_json, type(text_data_json))
            if type(text_data_json) != dict:
                print(2)
                self.disconnect(
                    'Text json is not dict format'
                )
                return
            print(3)
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_name,
                self.channel_name,
            )
            print('--text_data_json', type(text_data_json))
            websocket_connectivity(
                text_json=text_data_json
            )
        except Exception as e:
            self.disconnect(
                close_code=f"Receiver was disconnected due to , {str(e)}")

    def disconnect(self, close_code="Web disconnected"):
        print("websocket is disconnected", close_code)
        self.conversation_name = "data_sync"
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )
        async_to_sync(self.channel_layer.group_send)(
            self.conversation_name,
            {
                "type": "sender_layer",
                "conversations": self.conversation_name,
                "data": {
                    "status_code": 400,
                    "message": close_code,
                    "buffer_data": None
                }
            },
        )

    def sender_layer(self, event):
        self.send(text_data=json.dumps(event))
