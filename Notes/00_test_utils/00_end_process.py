import glob, os, time
from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def remove_empty_lines(text):
    # Split the text into lines
    lines = text.splitlines()
    
    # Filter out empty lines and lines with only whitespace
    non_empty_lines = [line for line in lines if line.strip()]
    
    # Join the non-empty lines back together
    cleaned_text = "".join(non_empty_lines)
    
    return cleaned_text

def save_encrypt_data(file_name, data):
    with open(file_name, 'w') as key_file:
        key_file.write(data)

# # Function to generate a key
# def generate_key():
#     key = Fernet.generate_key()
#     with open('secret.key', 'wb') as key_file:
#         key_file.write(key)
#     # print(f'Key generated and saved to secret key: {key.decode()} \t Data Type : {type(key)} || {type(key.decode())}')
#     return key

# # Function to load the key
# def load_key():
#     return open('secret.key', 'rb').read()

# # Function to encrypt data
# def encrypt_data(data, key):
#     f = Fernet(key)
#     encrypted_data = f.encrypt(data.encode('utf-8'))
#     return encrypted_data




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

if __name__ == "__main__":

    # taday_date = '20240516'
    # f_path = 'extractions/cadpad/'

    directory = 'encrypt_data_folder' # os.path.join(f_path, taday_date)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for name in glob.glob('Flask Restful API/*'):
        if os.path.isfile(name):
            # print("\n", name)
            f = open(name, "r")
            line_concat = ''
            for x in f:
                line_concat = line_concat + x
                # line_concat = remove_empty_lines(line_concat)
                # print(x)
            
            # print("------------------", "\n")

            # # Generate and save a key (do this once and keep the key safe)
            # key = generate_key()

            # # Load the key (do this whenever you need to encrypt or decrypt)
            # key = load_key()

            # # Data to encrypt
            # original_data = line_concat
            # # print(line_concat)

            # # Encrypt the data
            # encrypted_data = encrypt_data(original_data, key)
            # # print(f'Encrypted data: {encrypted_data} \n{encrypted_data.decode()}')  

            original_data = line_concat
            password = "ABmSxC7ULg5MWN3W62nQf8y5uXBl2Ag"
            
            # Encrypt the data
            encrypted_data = encrypt_data(original_data, password)
            # print(f'Encrypted data: {encrypted_data}')
            
            # print(f'{key.decode()} || {encrypted_data.decode()}')  
            # print(f'{password} || {encrypted_data}')  

            data_string = f'>> {encrypted_data}'

            f_path = name.split('\\')[1].split('.')[0] + '.txt'
            file_name = os.path.join(directory, f_path)
            save_encrypt_data(file_name, data_string)

            # print("------------------", "\n")

        # break

