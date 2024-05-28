import base64

# Function to generate a simple key (XOR key)
def generate_key(length):
    return bytearray([i % 256 for i in range(length)])

# Function to encrypt data using XOR and encode it with Base64
def encrypt_data(data, key):
    byte_data = data.encode('utf-8')
    encrypted_data = bytearray([byte_data[i] ^ key[i % len(key)] for i in range(len(byte_data))])
    encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
    return encoded_data

# Function to decrypt data using Base64 and XOR
def decrypt_data(encoded_data, key):
    encrypted_data = base64.b64decode(encoded_data)
    decrypted_data = bytearray([encrypted_data[i] ^ key[i % len(key)] for i in range(len(encrypted_data))])
    return decrypted_data.decode('utf-8')

# Example usage
if __name__ == "__main__":
    # Original data
    original_data = "This is a secret message."

    # Generate a simple key
    key = generate_key(len(original_data))
    print(f'Key generated and saved to secret.key: {key}')

    # Encrypt the data
    encrypted_data = encrypt_data(original_data, key)
    print(f'Encrypted data: {encrypted_data}')

    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, key)
    print(f'Decrypted data: {decrypted_data}')
