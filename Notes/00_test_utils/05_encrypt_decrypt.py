from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import base64

# Function to derive a key from a password
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Function to encrypt data
def encrypt_data(data, password):
    # Generate a random salt
    salt = os.urandom(16)
    # Derive a key from the password
    key = derive_key(password, salt)
    
    # Generate a random IV
    iv = os.urandom(12)
    
    # Create AES-GCM cipher
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    
    # Encrypt the data
    ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
    
    # Return the encrypted data along with the salt, IV, and tag
    return base64.b64encode(salt + iv + encryptor.tag + ciphertext).decode('utf-8')

# Function to decrypt data
def decrypt_data(encoded_data, password):
    # Decode the base64 encoded data
    data = base64.b64decode(encoded_data)
    
    # Extract the salt, IV, tag, and ciphertext
    salt = data[:16]
    iv = data[16:28]
    tag = data[28:44]
    ciphertext = data[44:]
    
    # Derive the key from the password and salt
    key = derive_key(password, salt)
    
    # Create AES-GCM cipher
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data.decode('utf-8')

# Example usage
if __name__ == "__main__":
    original_data = "This is a secret message."
    password = "strongpassword"
    
    # Encrypt the data
    encrypted_data = encrypt_data(original_data, password)
    print(f'Encrypted data: {encrypted_data}')
    
    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, password)
    print(f'Decrypted data: {decrypted_data}')
