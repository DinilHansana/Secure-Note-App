import hashlib
import os
import pyotp
import qrcode
from PIL import Image
from config import QR_FOLDER, PBKDF2_ITERATIONS

def hash_password(password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, PBKDF2_ITERATIONS)
    return salt, hashed

def verify_password(password: str, salt: bytes, hashed: bytes) -> bool:
    test_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, PBKDF2_ITERATIONS)
    return test_hash == hashed


def generate_2fa_secret() -> str:
    return pyotp.random_base32()

def get_2fa_uri(secret: str, username: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="SecureNoteApp")

def generate_qr_code(uri: str, username: str) -> str:
    path = os.path.join(QR_FOLDER, f"{username}_2fa.png")
    qr = qrcode.make(uri)
    qr.save(path)
    print(f"QR saved to: {path}")
    return path

def verify_2fa_token(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
