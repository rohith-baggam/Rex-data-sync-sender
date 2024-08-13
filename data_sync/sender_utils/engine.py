from core.settings import (
    DATA_SYNC_RECEIVER_TOKEN,
    SECRET_KEY
)
from data_sync.sender_utils.schema_verification import (
    get_model_properties
)
from django_data_seed.utils.json_compare import (
    compare_json_objects
)
from .utils import (
    convert_string_to_json,
    get_model_with_name
)
from data_sync.sender_utils.cipher import decrypt_data
socket_response = {
    'status_code': 400,
    'message': "",
    'buffer_data': None
}


def token_verification(text_json: dict) -> dict:
    """
        verify token which comes from receiver
    """
    if 'token' not in text_json:
        socket_response['status_code'] = 400
        socket_response['message'] = "Token not found"
        return socket_response

    if DATA_SYNC_RECEIVER_TOKEN == decrypt_data(text_json['token']):
        socket_response['status_code'] = 200
        socket_response['message'] = "Token is sucessfully verified"
        return socket_response
    socket_response['status_code'] = 400
    socket_response['message'] = "Incorrect Token"
    return socket_response


def secret_key_verification(text_json: dict) -> tuple:
    """
        verify secret key of receivers project
    """
    if not text_json.get('data') or not text_json['data'].get('SECRET_KEY'):
        socket_response['status_code'] = 400
        socket_response["message"] = "Secret key not found"
        return socket_response

    if SECRET_KEY == decrypt_data(text_json['data']['SECRET_KEY']):
        socket_response["message"] = "Secret key matched sucessfully"
        socket_response['status_code'] = 200
        return socket_response
    socket_response['status_code'] = 400
    socket_response["message"] = "Secret keys is not matching"
    return socket_response


def schema_verification(text_json: dict) -> tuple:
    try:
        if not text_json.get('data') or not text_json['data'].get('model_meta_data'):
            socket_response['status_code'] = 400
            socket_response["message"] = "Model Meta Data not found"
            return socket_response
        # ? decrypt model properties given by receiver
        receiver_model_meta_data = decrypt_data(
            text_json['data']['model_meta_data'])
        # ? get model instance with model name
        model = get_model_with_name(receiver_model_meta_data['model'])
        # ? if receiver model is not in sender models then return error
        if not model:
            socket_response['status_code'] = 400
            socket_response["message"] = "Model not found"
            return socket_response
        # ? if model exists get model properties
        sender_model_meta_data = get_model_properties(
            model[0]
        )
        # ? compare sender and receiver model properties
        if compare_json_objects(
            obj1=sender_model_meta_data,
            obj2=receiver_model_meta_data
        ):
            socket_response['status_code'] = 200
            socket_response["message"] = "Model Meta Data Matched sucessfully"
            return socket_response
        socket_response['status_code'] = 400
        socket_response["message"] = "Model Meta Data Properties are not matching"
        return socket_response
    except Exception as e:
        socket_response['status_code'] = 400
        socket_response["message"] = f"Incorrect Json format, {str(e)}"
        return socket_response
