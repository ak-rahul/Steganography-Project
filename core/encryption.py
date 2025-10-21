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
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: User password
            salt: Salt for key derivation (generated if None)
            
        Returns:
            Tuple of (key, salt)
        """
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
        """
        Encrypt message with password
        
        Args:
            message: Plain text message
            password: Encryption password
            
        Returns:
            Encrypted message with salt prepended
        """
        key, salt = PasswordEncryption.derive_key(password)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(message.encode())
        
        # Prepend salt to encrypted data
        return base64.b64encode(salt + encrypted).decode()
    
    @staticmethod
    def decrypt_message(encrypted_message: str, password: str) -> str:
        """
        Decrypt message with password
        
        Args:
            encrypted_message: Encrypted message with salt
            password: Decryption password
            
        Returns:
            Decrypted plain text message
            
        Raises:
            ValueError: If decryption fails
        """
        try:
            # Decode and extract salt
            data = base64.b64decode(encrypted_message.encode())
            salt = data[:16]
            encrypted = data[16:]
            
            # Derive key and decrypt
            key, _ = PasswordEncryption.derive_key(password, salt)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted)
            
            return decrypted.decode()
        except Exception as e:
            raise ValueError("Incorrect password or corrupted data")
