import qrcode
from PIL import Image
import base64

face = Image.open('logo.jpg')  # .crop((175, 90, 235, 150))

newsize = (75, 75)

face = face.resize(newsize)

qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

qr_big.add_data('https://www.youtube.com/watch?v=Rs3GfkHRwXA')

qr_big.make()

img_qr_big = qr_big.make_image().convert('RGB')

pos = ((img_qr_big.size[0] - face.size[0]) // 2, (img_qr_big.size[1] - face.size[1]) // 2)

img_qr_big.paste(face, pos)
img_qr_big.save('QR2.jpg')

with open("QR2.jpg", "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())

print('data:image/png;base64,',b64_string.decode('utf-8'))
