from cryptography.fernet import Fernet

# Function to generate a key
def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    print(f'Key generated and saved to secret key: {key.decode()}')
    return key

# Function to load the key
def load_key():
    return open('secret.key', 'rb').read()

# Function to encrypt data
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode('utf-8'))
    return encrypted_data

# Function to decrypt data
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data

# Example usage
if __name__ == "__main__":
    # Generate and save a key (do this once and keep the key safe)
    key = generate_key()

    # Load the key (do this whenever you need to encrypt or decrypt)
    key = load_key()

    # Data to encrypt
    original_data = "This is a secret message."

    # Encrypt the data
    encrypted_data = encrypt_data(original_data, key)
    print(f'Encrypted data: {encrypted_data}')

    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, key)
    print(f'Decrypted data: {decrypted_data}')
