import json
import ast
from django.apps import apps


def convert_nested_string_to_json(data):
    # Recursively process dictionary
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_nested_string_to_json(value)
        return data
    # Recursively process list
    elif isinstance(data, list):
        return [convert_nested_string_to_json(item) for item in data]
    # Convert string representation of a dict or list
    elif isinstance(data, str):
        try:
            # Attempt to parse as JSON
            parsed_data = json.loads(data)
            return convert_nested_string_to_json(parsed_data)
        except (json.JSONDecodeError, ValueError):
            try:
                # Attempt to evaluate Python dict-like string
                parsed_data = ast.literal_eval(data)
                return convert_nested_string_to_json(parsed_data)
            except (ValueError, SyntaxError):
                return data
    else:
        return data


def convert_string_to_json(data: str) -> dict:
    # First, parse the outermost JSON
    json_data = json.loads(data)
    # Then recursively convert any nested string representations
    json_data = convert_nested_string_to_json(json_data)
    print('json_data', type(json_data), json_data)
    return json_data


def get_model_with_name(model_name):
    installed_apps = [
        app_config.name for app_config in apps.get_app_configs()
    ]
    print(installed_apps)
    # print(apps.get_models())
    # for model in apps.get_models():
    #     print(str(model), str(model) in model_name)

    models = [
        model for model in apps.get_models()
        if model._meta.app_label in installed_apps and (not model_name or model_name in str(model))
    ]
    print('-m-', models)
    return models
