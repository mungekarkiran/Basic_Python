# # Install the required packages
# !sudo apt install tesseract-ocr
# !sudo apt install libtesseract-dev
# !sudo apt-get install tesseract-ocr

# !pip install pytesseract 
# !pip install pdf2image
# !pip install easyocr 
# !pip install tabula-py
# !pip install openpyxl 
# !pip install PyPDF2==2.12.1
# !pip install PyMuPDF

# !pip install pyngrok

# ===================================

import zipfile
zip_ref = zipfile.ZipFile("/content/drive/MyDrive/Colab Notebooks/OCR/Deployment.zip", 'r')
zip_ref.extractall()
zip_ref.close()
print('done...')

# ===================================

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from pyngrok import ngrok
from OCR_utils import *
import os

# Define a flask app
app = Flask(__name__)

# start ngrok when app is run
port_no = 5000
ngrok.set_auth_token("2KdKVvWPZia5YkGnclMcSmJGTjF_7XRGo19n8sau4r29JNaPL")
public_url =  ngrok.connect(port_no).public_url

@app.route('/', methods=['GET'])
def index():
  # Main page
  return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    # Get the file from post request
    f = request.files['file']
    
    file_path = os.path.join('static', secure_filename(f.filename))
    # Save the file to ./uploads
    f.save(file_path)

    # convert file to excel
    result = convert_to_excel(file_path)

    image_file_path = result["input_image"][7:]
    output_file_path = result["display_image"][7:]
    detected_words = result["detected_words"]
    download_file_path = result["download_excel"][7:]

    return render_template('index.html', file_path=image_file_path, 
                           output_file_path=output_file_path, 
                           detected_words=detected_words, 
                           download_file=download_file_path)
  return None

if __name__ == '__main__':
  print(f"To acces the Gloable link please click {public_url}")
  app.run(port=port_no)
