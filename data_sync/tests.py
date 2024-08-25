from django.test import TestCase
from django.core.management import call_command
from data_sync.receiver_utils.cipher import (
    encrypt_data,
    decrypt_data
)
from core.settings import DATA_SYNC_RECEIVER_TOKEN
# Create your tests here.


class DataSyncSenderTestCase(TestCase):
    def setUp(self):
        call_command(
            'seeddata',
            '--no-of-objects',
            '10'
        )

    def test_sender_functionality(self):
        # ? Verify token configuration
        self.assertEqual(bool(DATA_SYNC_RECEIVER_TOKEN), True,
                         "Receiver token configuration is missing.")
        self.stdout_info('Configuration check passed: Sender token found.')

        # ? Test encryption and decryption consistency
        data = 'Test data to encrypt'
        test_1_encrypt_data = encrypt_data(data)
        test_2_encrypt_data = encrypt_data(data)

        # ? Ensure the encryption generates unique hashes
        self.assertNotEqual(
            test_1_encrypt_data,
            test_2_encrypt_data,
            "Encryption check failed: Identical data should not produce the same hash."
        )
        self.stdout_success(
            'Encryption check passed: Unique hashes generated for identical data.')

        # ? Ensure that even with different hashes, decryption results are the same
        self.assertEqual(
            decrypt_data(test_1_encrypt_data),
            decrypt_data(test_2_encrypt_data),
            "Decryption consistency check failed: Decrypted results should be identical despite different hashes."
        )
        self.stdout_success(
            'Decryption consistency check passed: Identical results obtained after decrypting different hashes.')

        # ? Ensure the decrypted data matches the original input
        self.assertEqual(
            data,
            decrypt_data(test_1_encrypt_data),
            "Final decryption check failed: Decrypted data does not match the original input."
        )
        self.stdout_success(
            'Final decryption check passed: Data decrypted successfully.')
