
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from data_sync.sender_utils import engine

channel_layer = get_channel_layer()
socket_response = {

}


def broadcast_data(messsage_object: dict, socket_type: str) -> None:
    """
        Broadcast data from here
    """

    conversation_name = 'data_sync'
    try:
        async_to_sync(channel_layer.group_send)(
            conversation_name,
            {
                "type": socket_type,
                "conversations": conversation_name,
                "data": messsage_object
            },
        )
    except Exception as e:
        print('broadcast_data', e)


def websocket_connectivity(text_json: dict) -> None:
    function_name = str(text_json['data']['type']).lower()
    # ? call engine methods to begin process
    if hasattr(engine, function_name):
        engine_function = getattr(engine, function_name)
        messsage_object = engine_function(text_json)

        broadcast_data(messsage_object=messsage_object,
                       socket_type=function_name)
