"""Password-based encryption module using AES"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


class PasswordEncryption:
    """AES encryption with password-based key derivation"""
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    @staticmethod
    def encrypt_message(message: str, password: str) -> str:
        key, salt = PasswordEncryption.derive_key(password)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(message.encode())
        return base64.b64encode(salt + encrypted).decode()
    
    @staticmethod
    def decrypt_message(encrypted_message: str, password: str) -> str:
        try:
            data = base64.b64decode(encrypted_message.encode())
            salt = data[:16]
            encrypted = data[16:]
            
            key, _ = PasswordEncryption.derive_key(password, salt)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted)
            
            return decrypted.decode()
        except Exception:
            raise ValueError("Incorrect password or corrupted data")
