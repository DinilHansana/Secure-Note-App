from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_LENGTH = 32  
PBKDF2_ITERATIONS = 100000

def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=KEY_LENGTH, count=PBKDF2_ITERATIONS)

def encrypt_note(plaintext: str, password: str) -> str:
    salt = get_random_bytes(SALT_SIZE)
    nonce = get_random_bytes(NONCE_SIZE)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())

    final = salt + nonce + tag + ciphertext
    return base64.b64encode(final).decode()

def decrypt_note(encrypted_b64: str, password: str) -> str:
    try:
        raw = base64.b64decode(encrypted_b64)
        salt = raw[:SALT_SIZE]
        nonce = raw[SALT_SIZE:SALT_SIZE+NONCE_SIZE]
        tag = raw[SALT_SIZE+NONCE_SIZE:SALT_SIZE+NONCE_SIZE+16]
        ciphertext = raw[SALT_SIZE+NONCE_SIZE+16:]
        key = derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode()
    except Exception:
        return "[Decryption Failed]"
