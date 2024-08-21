import json
import inspect
from typing import Any
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
    get_model_with_name,
    dump_data
)
from data_sync.sender_utils.cipher import (
    decrypt_data,
    encrypt_data
)


socket_response = {
    'status_code': 400,
    'message': "",
    'buffer_data': None
}


def token_verification(text_json: dict) -> dict:
    """
        Arg:
            - text_json : Payload from the socket
        Info:
            - verify token which comes from receiver
        Result:
            - A dict which contains broadcast information
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
        Arg:
            - text_json : Payload from the socket
        Info:
            - verify secret key of receivers project
        Result:
            - A dict which contains broadcast information
    """
    if not text_json.get('data') or not text_json['data'].get('SECRET_KEY'):
        socket_response['status_code'] = 400
        socket_response["message"] = "Secret key not found"
        return socket_response
    if SECRET_KEY == decrypt_data(
        text_json['data']['SECRET_KEY']
    ):
        socket_response["message"] = "Secret key matched sucessfully"
        socket_response['status_code'] = 200
        return socket_response
    socket_response['status_code'] = 400
    socket_response["message"] = "Secret keys is not matching"
    return socket_response


def schema_verification(text_json: dict) -> tuple:
    """
        Arg:
            - text_json : Payload from the socket
        Info:
            - This function takes model information from text_json and 
              and compare the receiver model schema information with 
              sender model schema information 
        Result:
            - A dict which contains broadcast information
    """
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


def load_json_dump(filename: str = 'dump_data.json') -> list:
    """
        Load a JSON dump file and return its contents as a list of objects.

        Args:
            filename (str): The path to the JSON dump file. Defaults to 'dump_data.json'.

        Returns:
            list: A list of objects parsed from the JSON file.
    """
    try:
        with open(filename, 'r') as file:
            # ? Load the JSON data from the file
            data = json.load(file)
            # ? Ensure data is a list
            if isinstance(data, list):
                return data
            else:
                raise ValueError("The JSON file does not contain a list.")
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except ValueError as e:
        return []


def data_transformation_successful(text_data: dict) -> dict:
    socket_response['status_code'] = 200
    socket_response['message'] = "Data Transformation is Done Successfully"
    # ? to avoid circular dependency import function inside current function
    from data_sync.sender_utils.websocket_utils import broadcast_data
    broadcast_data(
        messsage_object=socket_response,
        socket_type=str(
            inspect.currentframe(
            ).f_code.co_name
        ).upper()
    )
    return socket_response


def get_buffer_data_for_index(index: int) -> dict:
    try:
        # ? length of instances to transfor
        all_instance = len(load_json_dump())
        if index <= all_instance:
            # ? get object of specific instance
            data = load_json_dump()[index]
            # ? transformation percentage calculation
            percentage = int(
                (
                    int(
                        index+1
                    )/all_instance
                )*100
            )
            socket_response['message'] = f'{percentage} %'
            socket_response['instance'] = f"{str(index+1)}/{str(all_instance)}"
            socket_response['status_code'] = 200
            socket_response['buffer_data'] = encrypt_data(data)
        else:
            return data_transformation_successful()
    except Exception as e:
        socket_response['message'] = f"Incorrect Index, {str(e)}"
        socket_response['status_code'] = 400
    return socket_response


def data_information(text_data: dict) -> dict:
    socket_response['message'] = "Transforing model information"
    socket_response['status_code'] = 200
    # ? dump entire database into json
    dump_data()
    # ? send length of json data
    socket_response['model_meta_data'] = encrypt_data(len(
        load_json_dump(
        )
    ))
    return socket_response


def data_transformation(text_data: dict) -> dict:
    try:
        model_meta_data = text_data['data']['model_meta_data']
        if 'index' not in model_meta_data:
            socket_response['message'] = 'Index is required'
            socket_response['status_code'] = 400
            return socket_response
        return get_buffer_data_for_index(decrypt_data(model_meta_data['index']))
    except Exception as e:
        socket_response['message'] = f"Incorrect Format, {str(e)}"
        socket_response['status_code'] = 400
        return socket_response
