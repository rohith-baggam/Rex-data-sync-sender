# from django.test import TestCase
# from django.core.management import call_command

# from data_sync.sender_utils.engine import (
#     token_verification,
#     secret_key_verification,
#     schema_verification,
#     data_information,
#     load_json_dump,
#     get_buffer_data_for_index
# )
# # Create your tests here.


# class DataSyncReceiverScriptTestCase(TestCase):
#     def setUp(self):

#         call_command(
#             'seeddata'
#         )

#     def test_token(self):
#         # ? token verification
#         script_function = {
#             "token_verification": {
#                 'function': token_verification,
#                 'success_message': 'Token verified successfully',
#                 'error_message': 'Incorrect token'
#             },
#             "secret_key_verification": {
#                 'function': secret_key_verification,
#                 'success_message': 'Secret key verified successfully',
#                 'error_message': 'Secret key token'
#             },
#             "schema_verification": {
#                 'function': schema_verification,
#                 'success_message': 'Schema verified successfully',
#                 'error_message': 'Schema is not matching'
#             },
#             'load_json_dump': {
#                 'function': load_json_dump,
#                 'success_message': 'Loadded data successfully',
#                 'error_message': 'Error while loading data'
#             },
#             "data_information": {
#                 'function': data_information,
#                 'success_message': 'Data packets count received successfully',
#                 'error_message': 'Schema is not matching'
#             },
#             "get_buffer_data_for_index" : {
#                 'function' : get_buffer_data_for_index,
#                 'success_message' : 'Data packet found for a specific index',
#                 'error _message' : ''
#             }
#         }
#         return
