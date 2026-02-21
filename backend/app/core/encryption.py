"""
NoorGuard Ultimate - Encryption Module
AES-256 Encryption for Data Protection
"""

import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

from app.core.config import settings


class AES256Encryption:
    """AES-256 encryption implementation"""
    
    def __init__(self, key: str = None):
        """
        Initialize encryption with a key
        
        Args:
            key: 32-byte key for AES-256 (will be hashed if shorter)
        """
        if key is None:
            key = settings.aes_key
        
        # Ensure key is 32 bytes
        if len(key) < 32:
            key = hashlib.sha256(key.encode()).digest()
        else:
            key = key[:32].encode()
        
        self.key = key
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using AES-256-CBC
        
        Args:
            plaintext: String to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        
        # Pad plaintext
        plaintext_bytes = plaintext.encode('utf-8')
        padding_length = 16 - (len(plaintext_bytes) % 16)
        plaintext_bytes += bytes([padding_length] * padding_length)
        
        # Encrypt
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()
        
        # Combine IV and ciphertext
        combined = iv + ciphertext
        
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt(self, encrypted: str) -> str:
        """
        Decrypt AES-256-CBC encrypted string
        
        Args:
            encrypted: Base64 encoded encrypted string
            
        Returns:
            Decrypted plaintext
        """
        # Decode from base64
        combined = base64.b64decode(encrypted.encode('utf-8'))
        
        # Extract IV and ciphertext
        iv = combined[:16]
        ciphertext = combined[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        
        # Decrypt
        decryptor = cipher.decryptor()
        plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        padding_length = plaintext_bytes[-1]
        plaintext_bytes = plaintext_bytes[:-padding_length]
        
        return plaintext_bytes.decode('utf-8')
    
    def encrypt_dict(self, data: dict) -> str:
        """Encrypt a dictionary as JSON string"""
        import json
        return self.encrypt(json.dumps(data))
    
    def decrypt_dict(self, encrypted: str) -> dict:
        """Decrypt to a dictionary"""
        import json
        decrypted = self.decrypt(encrypted)
        return json.loads(decrypted)


class FernetEncryption:
    """Fernet (symmetric) encryption for sensitive data"""
    
    def __init__(self, key: str = None):
        """
        Initialize Fernet encryption
        
        Args:
            key: Key for encryption (will be base64 encoded)
        """
        if key is None:
            key = settings.encryption_key
        
        # Generate key from password
        key_bytes = hashlib.sha256(key.encode()).digest()
        self.fernet = Fernet(base64.urlsafe_b64encode(key_bytes))
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt string using Fernet"""
        return self.fernet.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, encrypted: str) -> str:
        """Decrypt Fernet encrypted string"""
        return self.fernet.decrypt(encrypted.encode()).decode()
    
    def encrypt_bytes(self, data: bytes) -> bytes:
        """Encrypt bytes"""
        return self.fernet.encrypt(data)
    
    def decrypt_bytes(self, encrypted: bytes) -> bytes:
        """Decrypt bytes"""
        return self.fernet.decrypt(encrypted)


class HashUtils:
    """Hashing utilities for passwords and data"""
    
    @staticmethod
    def sha256(data: str) -> str:
        """Generate SHA-256 hash"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def sha512(data: str) -> str:
        """Generate SHA-512 hash"""
        return hashlib.sha512(data.encode()).hexdigest()
    
    @staticmethod
    def md5(data: str) -> str:
        """Generate MD5 hash"""
        return hashlib.md5(data.encode()).hexdigest()
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a secure random token"""
        return os.urandom(length).hex()


class DataMasker:
    """Mask sensitive data for logging/display"""
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address"""
        if '@' not in email:
            return email
        
        local, domain = email.split('@')
        if len(local) <= 2:
            masked_local = '*' * len(local)
        else:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
        
        return f"{masked_local}@{domain}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """Mask phone number"""
        if len(phone) < 4:
            return '*' * len(phone)
        
        return '*' * (len(phone) - 4) + phone[-4:]
    
    @staticmethod
    def mask_card(card: str) -> str:
        """Mask credit card number"""
        if len(card) < 4:
            return '*' * len(card)
        
        return '*' * (len(card) - 4) + card[-4:]


# Singleton instances
aes_encryption = AES256Encryption()
fernet_encryption = FernetEncryption()
hash_utils = HashUtils()
data_masker = DataMasker()
