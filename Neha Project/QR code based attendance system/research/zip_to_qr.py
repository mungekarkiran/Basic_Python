import zipfile
import qrcode

def create_qr_code(zip_file_path, qr_code_image_path):
    # Read the ZIP file and convert it to bytes
    with open(zip_file_path, 'rb') as zip_file:
        zip_data = zip_file.read()

    # Create a QR code with the ZIP file data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(zip_data)
    qr.make(fit=True)

    # Create an image from the QR code and save it
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_code_image_path)

if __name__ == "__main__":
    zip_file_path = "file.zip"
    qr_code_image_path = "qrcode.png"

    create_qr_code(zip_file_path, qr_code_image_path)
