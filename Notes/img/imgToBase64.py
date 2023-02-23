import base64

with open('img1.jpg', 'rb') as f:
    data = f.read()

base64_image = base64.b64encode(data).decode('utf-8')
print(f"base64_image : {base64_image}")

# base32_image = base64.b32encode(data).decode('utf-8')
# print(f'Base32-encoded image: {base32_image}')

# Audio to base64
# get sample sample audio file
# https://voiceage.com/Audio-Samples-AMR-WB.html

# Read the audio file
with open('audio_file.wav', 'rb') as f:
    audio_bytes = f.read()

# Convert audio to base64
audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
# Print the base64-encoded audio
print(audio_base64)


# https://samplelib.com/sample-mp4.html
# Read the audio file
with open('video_file.mp4', 'rb') as f:
    video_bytes = f.read()

# Convert video to base64
video_base64 = base64.b64encode(video_bytes).decode('utf-8')
# Print the base64-encoded video
print(video_base64)



html = f'''
<!DOCTYPE html>
<html>
<head>
	<title>Image to Base64</title>
</head>
<body>
	<img id="image" src="data:image/jpeg;base64,{base64_image}">
    <br><br>
    <audio controls>
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
        Your browser does not support the audio element.
    </audio>
    <br><br>
    <video controls>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>

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
