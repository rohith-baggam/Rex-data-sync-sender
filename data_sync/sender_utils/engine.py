from core.settings import (
    DATA_SYNC_RECEIVER_TOKEN,
    SECRET_KEY
)

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

    if DATA_SYNC_RECEIVER_TOKEN == text_json['token']:
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

    if SECRET_KEY == text_json['data']['SECRET_KEY']:
        socket_response["message"] = "Secret key matched sucessfully"
        socket_response['status_code'] = 200
        return socket_response
    socket_response['status_code'] = 400
    socket_response['"message"'] = "Secret keys is not matching"
    return socket_response
