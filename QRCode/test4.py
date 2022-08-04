# import base64
# from io import BytesIO, StringIO
# from PIL import Image

# # image_string = StringIO(base64.b64decode('logo.jpg'))
# image = Image.open('logo.jpg')
# angle = 90
# rotated_image = image.rotate( angle, expand=1 )


# buffered = BytesIO()
# image.save(buffered, format="JPEG")
# img_str = base64.b64encode(buffered.getvalue())

# print(img_str)




# import base64


# with open("qr_lena2.png", "rb") as image2string:
# 	converted_string = base64.b64encode(image2string.read())
# print(converted_string)

# with open('encode.bin', "wb") as file:
# 	file.write(converted_string)


# b64_string = """
# hello
# kiran

# """
# image_code  = base64.b64decode(b64_string.replace("\n",""))
# with open('ENCODED1.txt', 'wb') as f:
#    f.write(image_code )



import base64

with open("qr_lena2.png", "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())
print(b64_string)
print("++++"*20)
print('data:image/png;base64,',b64_string.decode('utf-8'))