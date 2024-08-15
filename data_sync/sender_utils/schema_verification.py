
from django.db import models
from django.apps import apps

# TODO Updated schema verification with new logic current one is not returning for manytomany


def get_model_properties(model: models.Model) -> dict:
    """
    Retrieve and return all properties of a Django model, including fields, types, and attributes.
    """
    properties = {}
    # ? Get all fields of the model
    fields = model._meta.get_fields()
    for field in fields:
        field_info = {
            'type': type(field).__name__,
            'max_length': getattr(field, 'max_length', None),
            'null': getattr(field, 'null', None),
            'blank': getattr(field, 'blank', None),
            'default': getattr(field, 'default', None) if getattr(field, 'default', None) in [True, False] else str(getattr(field, 'default', None)),
            'unique': getattr(field, 'unique', None),
            'db_index': getattr(field, 'db_index', None),
            'related_name': getattr(field, 'related_name', None),
            'related_model': getattr(field.remote_field, 'model', None) if hasattr(field, 'remote_field') else None,
            # ? Get choices if available
            'choices': getattr(field, 'choices', None),
        }

        # ? If the field has choices, get the choices and default choice
        if field_info['choices']:
            field_info['choices'] = list(field_info['choices'])
            field_info['default_choice'] = field_info['default']
        properties[field.name] = field_info

    return {
        "model": "DataSyncTestBooleanModel",
        "fields": properties
    }
