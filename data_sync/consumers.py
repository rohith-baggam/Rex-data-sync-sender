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
        This websocket does sender action
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversation_name = None

    def connect(self):
        try:
            self.accept()
            query_string_bytes = self.scope.get("query_string", b"")
            query_string = parse_qs(query_string_bytes.decode("utf-8"))
            token_info = query_string.get("token", [None])[0]

            # if not token_info:
            #     self.close(code=4000)  # Use appropriate WebSocket close code
            #     return

            self.conversation_name = "data_sync"
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_name,
                self.channel_name
            )

            # async_to_sync(self.channel_layer.group_send)(
            #     self.conversation_name,
            #     {
            #         "type": "sender_layer",
            #         "conversations": self.conversation_name,
            #         "data": {
            #             "status_code": 200,
            #             "message": "Connected",
            #             "buffer_data": None
            #         }
            #     }
            # )
        except Exception as e:
            self.close(code=f"something went wrong in conncet, {str(e)}")
            # Use appropriate WebSocket close code
            print(f"Connection error: {e}")

    def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                text_data_json = convert_string_to_json(text_data)

                if not isinstance(text_data_json, dict):
                    # Use appropriate WebSocket close code
                    self.close(code=f"Incorrect format, {str(e)}")
                    return

                websocket_connectivity(text_json=text_data_json)
        except Exception as e:
            # Use appropriate WebSocket close code
            self.close(code=f"something went wrong in recieve, {str(e)}")
            print(f"Receive error: {e}")

    def disconnect(self, close_code=None):
        # if self.conversation_name:
        #     async_to_sync(self.channel_layer.group_discard)(
        #         self.conversation_name,
        #         self.channel_name
        #     )
        #     async_to_sync(self.channel_layer.group_send)(
        #         self.conversation_name,
        #         {
        #             "type": "sender_layer",
        #             "conversations": self.conversation_name,
        #             "message": "socket disconnected"
        #         }
        #     )
        # print("WebSocket is disconnected", close_code)
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

# class DataSyncSenderConsumer(WebsocketConsumer):

#     """
#         This web socket does sender action
#     """

#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.conversation_name = None

#     def connect(self):
#         try:
#             self.accept()
#             query_string_bytes = self.scope.get("query_string", b"")
#             query_string = parse_qs(query_string_bytes.decode("utf-8"))
#             token_info = query_string["token"][0]
#             print('token_info', token_info)
#             if token_info == False:
#                 self.disconnect("UNAUTHORIZED")
#             self.conversation_name = "data_sync"
#             async_to_sync(self.channel_layer.group_add)(
#                 self.conversation_name,
#                 self.channel_name,
#             )
#             async_to_sync(self.channel_layer.group_send)(
#                 self.conversation_name,
#                 {
#                     "type": "sender_layer",
#                     "conversations": self.conversation_name,
#                     "data": {
#                         "status_code": 200,
#                         "message": "Connected",
#                         "buffer_data": None
#                     }
#                 },
#             )
#         except Exception as e:

#             self.disconnect(
#                 close_code=f"Receiver was disconnected due to , {str(e)}")

#     def receive(self, text_data=None, bytes_data=None):
#         try:
#             try:
#                 print('text_data', text_data, type(text_data))
#                 text_data_json = convert_string_to_json(text_data)
#                 # text_data_json = text_data
#                 print(0)
#                 # text_data_json = json.loads(text_data)
#                 # text_data_json = json.dumps(text_data_json)
#             except Exception as e:
#                 print('Exception', e)
#                 text_data_json = {}
#                 self.disconnect(
#                     f'json convertion error, {str(e)}'
#                 )
#                 return
#             print(1, text_data_json, type(text_data_json))
#             if type(text_data_json) != dict:
#                 print(2)
#                 self.disconnect(
#                     'Text json is not dict format'
#                 )
#                 return
#             print(3)
#             async_to_sync(self.channel_layer.group_add)(
#                 self.conversation_name,
#                 self.channel_name,
#             )
#             print('--text_data_json', type(text_data_json))
#             websocket_connectivity(
#                 text_json=text_data_json
#             )
#         except Exception as e:
#             self.disconnect(
#                 close_code=f"Receiver was disconnected due to , {str(e)}")

#     def disconnect(self, close_code="Web disconnected"):
#         print("websocket is disconnected", close_code)
#         self.conversation_name = "data_sync"
#         async_to_sync(self.channel_layer.group_add)(
#             self.conversation_name,
#             self.channel_name,
#         )
#         async_to_sync(self.channel_layer.group_send)(
#             self.conversation_name,
#             {
#                 "type": "sender_layer",
#                 "conversations": self.conversation_name,
#                 "message": "socket disconnected"
#             },
#         )

#     def sender_layer(self, event):
#         self.send(text_data=json.dumps(event))
