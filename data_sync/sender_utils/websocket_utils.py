
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.settings import (
    DATA_SYNC_RECEIVER_TOKEN,
    SECRET_KEY
)
from data_sync.sender_utils import engine
channel_layer = get_channel_layer()
socket_response = {
    'status_code': 400,
    'message': "",
    'buffer_data': None
}


def broadcast_data(messsage_object: dict) -> None:
    """
        Broadcast data from here
    """
    conversation_name = 'data_sync'
    async_to_sync(channel_layer.group_send)(
        conversation_name,
        {
            "type": "sender_layer",
            "conversations": conversation_name,
            "data": messsage_object
        },
    )


def websocket_connectivity(text_json: dict) -> None:
    function_name = str(text_json['data']['type']).lower()
    # ? call engine methods to begin process
    if hasattr(engine, function_name):
        engine_function = getattr(engine, function_name)
        messsage_object = engine_function(text_json)
        broadcast_data(messsage_object=messsage_object)
    else:
        # ? Incorrect type received
        socket_response['status_code'] = 400
        socket_response['message'] = "Incorrect command"
        broadcast_data(
            messsage_object=socket_response
        )

# {
#     "STEP_1": "HAND_SHAKE",
#     "STEP_2": "TOKEN_VERIFICATION",
#     "STEP_3": "SECRET_KEY_VERIFICATION",
#     "STEP_4": "SCHEMA_VERIFICATION",
#     "SETP_5": "DATA_TRANFORMATION"

# }
