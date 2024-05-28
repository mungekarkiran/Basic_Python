from cryptography.fernet import Fernet

# Function to convert string to bytes
def string_to_bytes(input_string):
    # Encode the string to bytes using UTF-8 encoding
    byte_data = input_string.encode('utf-8')
    return byte_data

# Function to convert bytes back to string
def bytes_to_string(byte_data):
    # Decode the bytes to string using UTF-8 encoding
    decoded_string = byte_data.decode('utf-8')
    return decoded_string

# Function to decrypt data
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data


# Example usage
if __name__ == "__main__":
    
    key = 'TODh-AZVmebtliHFkJjDoKD4FJqqXflR0F9_wC6JOrM='
    data = 'gAAAAABmSxC7ULg5MWN3W62nQf8y5uXBl2AgBytDWQBzBKFlpMh5FeEsQHWOe0X8OFuPy9QR2RXTa3v3cDXi6VZlAWidywVzqPjchDJUPnzIcn4i--tgNO4='
    
    # Convert string to bytes
    key = string_to_bytes(key)
    encrypted_data = string_to_bytes(data)

    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, key)
    print(f'Decrypted data: {decrypted_data}')


        
    