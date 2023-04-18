from os import getenv
import base64
from cryptography.fernet import Fernet
key = getenv("ENCRYPTION_KEY").encode("UTF-8")


def get_recent_error(form):
    most_recent_error = None
    if form.errors:
        most_recent_error = tuple(form.errors.values())[0][-1]
    return most_recent_error


def encrypt_image(file: bytes) -> bytes:
    f = Fernet(key)
    encrypted = f.encrypt(file)
    return encrypted


def decrypt_image(image_bytes: bytes):
    f = Fernet(key)
    decrypted = f.decrypt(image_bytes)
    return base64.b64encode(decrypted).decode("utf-8")
