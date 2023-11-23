import cv2
import numpy as np
from pyzbar.pyzbar import decode
import zipfile
from io import BytesIO
import base64

def read_qr_code(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use pyzbar to decode QR code
    qr_codes = decode(gray)

    if qr_codes:
        return qr_codes[0].data.decode('utf-8')
    else:
        return None

def extract_zip_from_qr(qr_data, output_path):
    # Convert the base64-encoded string to bytes
    # zip_data = bytes(qr_data, 'utf-8')
    # Assuming qr_data is the base64-encoded string
    # zip_data = base64.b64decode(qr_data)
    # Assuming qr_data is the base64-encoded string
    # try:
    #     # Decode the base64 string with UTF-8 encoding
    #     zip_data = base64.b64decode(qr_data, validate=True).decode('utf-8')
    # except UnicodeDecodeError:
    #     print("Failed to decode base64 data with UTF-8 encoding.")
    #     # If UTF-8 decoding fails, you may need to try a different encoding based on your data
    # Assuming qr_data is the base64-encoded string
    try:
        # Decode the base64 string to binary data
        zip_data = base64.b64decode(qr_data, validate=True)
    except ValueError as e:
        print("Failed to decode base64 data.", e)
        # Handle the error appropriately

    # Extract the ZIP file content
    with zipfile.ZipFile(BytesIO(zip_data), 'r') as zip_ref:
        zip_ref.extractall(output_path)

if __name__ == "__main__":
    qr_code_image_path = "qrcode.png"
    output_path = "files"

    # Read QR code
    qr_data = read_qr_code(qr_code_image_path)

    if qr_data:
        # Extract ZIP file from QR code data
        extract_zip_from_qr(qr_data, output_path)
        print(f"ZIP file extracted to: {output_path}")
    else:
        print("No QR code found.")
