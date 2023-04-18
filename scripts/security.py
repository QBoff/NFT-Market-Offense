from os import getenv
import base64
from cryptography.fernet import Fernet
key = getenv("ENCRYPTION_KEY").encode("UTF-8")


def encrypt_image(file: bytes) -> bytes:
    f = Fernet(key)
    encrypted = f.encrypt(file)
    return encrypted


def decrypt_image(image_bytes: bytes):
    f = Fernet(key)
    decrypted = f.decrypt(image_bytes)
    return base64.b64encode(decrypted).decode("utf-8")
