import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from core.settings import SECRET_KEY
import os
import json


def encrypt_data(plain_text):
    # Convert the plain text (could be dict, list, etc.) to JSON string and then to bytes
    if not isinstance(plain_text, str):
        plain_text = json.dumps(plain_text)
    plain_bytes = plain_text.encode('utf-8')

    # Derive a key from the Django SECRET_KEY
    key = hashlib.sha256(SECRET_KEY.encode()).digest()

    # Generate a random initialization vector (IV)
    iv = os.urandom(16)

    # Create the cipher object and encrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(plain_bytes) + encryptor.finalize()

    # Combine the IV and encrypted bytes and encode to base64
    encrypted_data = base64.b64encode(iv + encrypted_bytes).decode('utf-8')
    return encrypted_data


def decrypt_data(encrypted_data):
    # Decode the base64 encoded data
    encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))

    # Derive a key from the Django SECRET_KEY
    key = hashlib.sha256(SECRET_KEY.encode()).digest()

    # Extract the IV from the beginning of the encrypted data
    iv = encrypted_bytes[:16]

    # Extract the actual encrypted bytes
    encrypted_bytes = encrypted_bytes[16:]

    # Create the cipher object and decrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

    # Convert the decrypted bytes back to plain text
    plain_text = decrypted_bytes.decode('utf-8')

    # Try to parse the plain text back to the original data type (dict, list, etc.)
    try:
        return json.loads(plain_text)
    except json.JSONDecodeError:
        return plain_text  # If it's not JSON, return as is
