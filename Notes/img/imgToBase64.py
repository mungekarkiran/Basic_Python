import base64

with open('img1.jpg', 'rb') as f:
    data = f.read()

base64_image = base64.b64encode(data).decode('utf-8')
print(f"base64_image : {base64_image}")

# base32_image = base64.b32encode(data).decode('utf-8')
# print(f'Base32-encoded image: {base32_image}')


html = f'''
<!DOCTYPE html>
<html>
<head>
	<title>Image to Base64</title>
</head>
<body>
	<img id="image" src="data:image/jpeg;base64,{base64_image}">
</body>
</html>
'''

with open('index.html', 'w') as f:
    f.write(html)

# ====================================
print('\n\n\n')
# ====================================

with open("img1.jpg", "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())
print(b64_string)
print("++++"*20)
print('data:image/png;base64,',b64_string.decode('utf-8'))
