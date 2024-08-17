from django.core.management.base import BaseCommand
from data_sync.sender_utils.engine import get_buffer_data_for_index
from data_sync.sender_utils.schema_verification import (
    get_model_properties
)
from data_sync.models import DataSyncTestBooleanModel
from data_sync.sender_utils.websocket_utils import (
    websocket_connectivity
)
from data_sync.sender_utils.utils import convert_string_to_json
from data_sync.sender_utils.cipher import encrypt_data
from pprint import pprint


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        pprint(get_buffer_data_for_index(438))
        # Example usage
        # from data_sync.models import DataSyncTestBooleanModel

        # Print the full path of the model class
        # print(self.get_model_full_path(DataSyncTestBooleanModel))
        # data = get_model_properties(
        #     model=DataSyncTestBooleanModel
        # )
        # print(data)
        # data = "django-insecure-39l1e#=blzk=m159qsk1dsm5ma74my&h@e)0oqi#pxnos=(zjt"
        # print(encrypt_data(data))
        # model_verification(
        #     text_json={
        #         "token": "f4b1e718-57bb-11ef-8d13-46124d953699",
        #         "data": {
        #             "type": "SECRET_KEY_VERIFICATION",
        #             "SECRET_KEY": "django-insecure-39l1e#=blzk=m159qsk1dsm5ma74my&h@e)0oqi#pxnos=(zjt"
        #         }
        #     }
        # )
