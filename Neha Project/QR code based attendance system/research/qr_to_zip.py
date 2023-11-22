import cv2
import numpy as np
from pyzbar.pyzbar import decode
import zipfile
from io import BytesIO

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
    zip_data = bytes(qr_data, 'utf-8')

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
