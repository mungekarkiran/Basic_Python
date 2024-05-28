# import qrcode

# # Read the content of the file
# with open('data.txt', 'r') as file:
#     data = file.read()

# # print(data.replace('\n', ''))

# # Generate the QR code
# qr = qrcode.QRCode(
#     # version=10,  # Controls the size of the QR Code
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
# )
# qr.add_data(data)
# qr.make(fit=True)

# # Create an image from the QR Code instance
# img = qr.make_image(fill_color="black", back_color="white")

# # Save the image to a file
# img.save('qrc.png')

# ======================================================

import qrcode
import zlib
import base64
import os, glob

if __name__ == "__main__":

    directory = 'qr_folder' # os.path.join(f_path, taday_date)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for name in glob.glob('encrypt_data_folder/*'):
        if os.path.isfile(name):
            print("\n", name)
            # f = open(name, "r")
            # for x in f:
            #     print(x)

            # Read the content of the file
            with open(name, 'r') as file:
                data = file.read()

            # Compress the data
            compressed_data = zlib.compress(data.encode('utf-8'))

            # Encode the compressed data to base64 to make it QR code friendly
            b64_data = base64.b64encode(compressed_data).decode('utf-8')

            # Generate the QR code
            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(b64_data)
            qr.make(fit=True)

            # Create an image from the QR Code instance
            img = qr.make_image(fill_color="black", back_color="white")

            f_path = name.split('\\')[1].split('.')[0] + '.png'
            file_name = os.path.join(directory, f_path)
            # Save the image to a file
            img.save(file_name)

            print(f'QR code generated and saved as {file_name}')

