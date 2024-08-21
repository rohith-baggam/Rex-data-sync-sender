from io import StringIO
from django.core.management import call_command
from core import settings
from django.db import models
import json
import ast
from django.apps import apps


def convert_nested_string_to_json(data):
    # ? Recursively process dictionary
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_nested_string_to_json(value)
        return data
    # ? Recursively process list
    elif isinstance(data, list):
        return [convert_nested_string_to_json(item) for item in data]
    # ? Convert string representation of a dict or list
    elif isinstance(data, str):
        try:
            # ? Attempt to parse as JSON
            parsed_data = json.loads(data)
            return convert_nested_string_to_json(parsed_data)
        except (json.JSONDecodeError, ValueError):
            try:
                # ? Attempt to evaluate Python dict-like string
                parsed_data = ast.literal_eval(data)
                return convert_nested_string_to_json(parsed_data)
            except (ValueError, SyntaxError):
                return data
    else:
        return data


def convert_string_to_json(data: str) -> dict:
    # ? First, parse the outermost JSON
    json_data = json.loads(data)
    # ? Then recursively convert any nested string representations
    json_data = convert_nested_string_to_json(json_data)
    return json_data


def get_model_with_name(model_name):
    # ? get all custom apps exclude package apps
    installed_apps = [
        app_config.name for app_config in apps.get_app_configs()
    ]
    # ? get all models of the custom Apps
    models = [
        model for model in apps.get_models()
        if model._meta.app_label in installed_apps and (not model_name or model_name in str(model))
    ]
    return models


def get_model_full_path(cls: models.Model):
    """
    Extract the full path of a Django model class from its class reference.

    Args:
        cls (type): The model class.

    Returns:
        str: The full path of the model in the format 'app_label.ModelName'.
    """
    # ? Get the module name
    module_name = cls.__module__
    # ? Get the class name
    class_name = cls.__qualname__.split('.')[-1]

    # ? The module_name is usually in the format 'app_name.models', so we extract 'app_name'
    app_label = module_name.split('.')[-2]

    # ? Return the formatted string
    return f"{app_label}.{class_name}"


def dump_data():
    # ? Get installed apps
    installed_apps = settings.INSTALLED_APPS

    # ? Filter out third-party apps by excluding apps that do not start with your project name or follow a specific pattern
    custom_apps = [app for app in installed_apps if not app.startswith(
        'third_party_prefix')]

    # ? Remove apps that are not relevant
    # ? For example, 'django.contrib.sites', 'rest_framework', etc., if you do not want to dump data for these
    # ? You might also want to exclude system or admin apps
    custom_apps = [app for app in custom_apps if not app.startswith(
        'django.') and not app.startswith('rest_framework')]

    all_data = []

    # ? Iterate through your custom apps and dump data
    for app in custom_apps:
        app_name = app.split('.')[-1]

        # ? Create a StringIO object to capture the output
        output = StringIO()

        # ? Call the 'dumpdata' command
        call_command('dumpdata', app_name, format='json', stdout=output)

        # ? Append the data from StringIO to the all_data list
        app_data = json.loads(output.getvalue())
        all_data.extend(app_data)

    # ? Write all collected data to a single JSON file
    with open('dump_data.json', 'w') as output_file:
        json.dump(all_data, output_file, indent=4)
