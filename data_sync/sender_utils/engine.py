import json
import inspect
from typing import Any
from decimal import Decimal
from django.db import models
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
    get_model_with_name,
    get_model_full_path,
    dump_data
)
from data_sync.sender_utils.cipher import (
    decrypt_data,
    encrypt_data
)
from django.apps import apps
from uuid import UUID


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
        print('sender_model_meta_data', sender_model_meta_data)
        print('receiver_model_meta_data', receiver_model_meta_data)
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


def send_buffer_data(queryset):
    for query in queryset:
        # ? Initialize the base response
        socket_response['status_code'] = 200
        socket_response['message'] = {
            'type': "DATA_TRANSFORMATION",
            'buffer_data': encrypt_data(
                {
                    'model': getattr(query, 'model', None),
                    'pk': getattr(query, 'pk', None),
                    'fields': getattr(query, 'fields', None),
                }
            )

        }

    return socket_response


def serialize_value(value, field):
    """
    Serialize a value based on its field type.

    Args:
        value: The value to serialize.
        field: The field for which the value is being serialized.

    Returns:
        The serialized value.
    """
    def is_json_serializable(obj: Any) -> bool:
        """Check if an object is JSON serializable."""
        try:
            json.dumps(obj)
            return True
        except (TypeError, OverflowError):
            return False
    return value if is_json_serializable(value) else str(value)


def get_model_pk_info():
    data_stat = []
    for model in apps.get_models():
        if model._meta.app_label in [app_config.name for app_config in apps.get_app_configs()]:
            # Get all instances of the model
            for query in model.objects.all():
                values = {}
                for field in model._meta.get_fields():
                    # Avoid handling reverse relationships and related managers
                    if field.is_relation and not field.many_to_many:
                        # Handle ForeignKey and OneToOneField
                        if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                            related_object = getattr(query, field.name, None)
                            if related_object:
                                values[field.name] = related_object.pk
                            else:
                                values[field.name] = None
                    elif field.many_to_many:
                        # Handle ManyToManyField
                        related_objects = getattr(query, field.name).all()
                        values[field.name] = [
                            obj.pk for obj in related_objects]
                    else:
                        # Handle other field types
                        values[field.name] = serialize_value(
                            getattr(query, field.name), field
                        )

                data_stat.append(
                    {
                        "model_name": get_model_full_path(model),
                        "pk": query.pk,
                        "fields": values
                    }
                )
    return data_stat


def get_count_of_all_instances():

    return sum(
        [
            model.objects.all().count()
            for model in apps.get_models()
            if model._meta.app_label in [
                app_config.name for app_config in apps.get_app_configs()
            ]
        ]
    )


def load_json_dump(filename='dump_data.json'):
    """
    Load a JSON dump file and return its contents as a list of objects.

    Args:
        filename (str): The path to the JSON dump file. Defaults to 'dump_data.json'.

    Returns:
        list: A list of objects parsed from the JSON file.
    """
    try:
        with open(filename, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
            # Ensure data is a list
            if isinstance(data, list):
                return data
            else:
                raise ValueError("The JSON file does not contain a list.")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON file.")
        return []
    except ValueError as e:
        print(f"Error: {e}")
        return []


def data_transformation_successful(text_data):
    socket_response['status_code'] = 200
    socket_response['message'] = "Data Transformation is Done Successfully"
    from data_sync.sender_utils.websocket_utils import broadcast_data
    broadcast_data(
        messsage_object=socket_response,
        socket_type=str(
            inspect.currentframe(
            ).f_code.co_name
        ).upper()
    )
    return socket_response


def get_buffer_data_for_index(index):
    try:

        all_instance = len(load_json_dump())
        print('index/all_instance', str(index), str(all_instance))
        if index <= all_instance:
            data = load_json_dump()[index]
            print('get_buffer_data_for_index', data)
            percentage = int(
                (int(index+1)/all_instance)*100
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


def data_information(text_data):
    socket_response['message'] = "Transforing model information"
    socket_response['status_code'] = 200
    dump_data()
    socket_response['model_meta_data'] = encrypt_data(len(
        load_json_dump(
        )
    ))
    return socket_response


def data_transformation(text_data):
    try:
        model_meta_data = text_data['data']['model_meta_data']
        print('model_meta_data', model_meta_data)
        if 'index' not in model_meta_data:
            socket_response['message'] = 'Index is required'
            socket_response['status_code'] = 400
            return socket_response
        return get_buffer_data_for_index(decrypt_data(model_meta_data['index']))
    except Exception as e:
        socket_response['message'] = f"Incorrect Format, {str(e)}"
        socket_response['status_code'] = 400
        return socket_response
