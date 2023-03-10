# LIBRARIES
import tabula
import pandas as pd
import glob, os, sys, fitz
import easyocr
import pytesseract
from PIL import Image
from openpyxl import Workbook
import subprocess
import uuid
import cv2

# VARIABLES
ROOT_PATH = os.getcwd()
STATIC_DIR = "static"

PDF_FILE_PATH = "/content/drive/MyDrive/Colab Notebooks/OCR/example2.pdf" 
IMG_FILE_PATH = "/content/drive/MyDrive/Colab Notebooks/OCR/example.jpg"

# EXCEL_FILE_NAME = "output.xlsx"
# CSV_FILE_NAME = "output.csv"
# IMAGE_FILE_NAME = "output.jpg"
# ZIP_FILE_NAME = "output_excel_file.zip"

# EXCEL_PATH = os.path.join(STATIC_DIR, EXCEL_FILE_NAME)
# CSV_PATH = os.path.join(STATIC_DIR, CSV_FILE_NAME)
# IMAGE_PATH = os.path.join(STATIC_DIR, IMAGE_FILE_NAME)
# ZIP_PATH = os.path.join(STATIC_DIR, ZIP_FILE_NAME)

# FUNCTIONS
def pdf_to_image(pdf_file_path):
  # To get better resolution
  zoom_x = 2.0  # horizontal zoom
  zoom_y = 2.0  # vertical zoom
  mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension
  # for filename in all_files:
  doc = fitz.open(pdf_file_path)  # open document
  IMAGE_FILE_NAME = f"pdf_to_image_{uuid.uuid4()}.jpg"
  IMAGE_PATH = os.path.join(STATIC_DIR, IMAGE_FILE_NAME)
  for page in doc:  # iterate through the pages
    pix = page.get_pixmap(matrix=mat)  # render page to an image
    pix.save(IMAGE_PATH)  # store image as a PNG
  print(f'Converted PDF file "{pdf_file_path}" to Image file "{IMAGE_PATH}"')
  return IMAGE_PATH

def pdf_to_excel(pdf_file_path):
  # file name and paths
  CSV_FILE_NAME = f"pdf_to_excel_{uuid.uuid4()}.csv"
  EXCEL_FILE_NAME = f"pdf_to_excel_{uuid.uuid4()}.xlsx"
  CSV_PATH = os.path.join(STATIC_DIR, CSV_FILE_NAME)
  EXCEL_PATH = os.path.join(STATIC_DIR, EXCEL_FILE_NAME)
  # Convert the PDF to a CSV file
  tabula.convert_into(pdf_file_path, CSV_PATH, output_format='csv', pages='all')
  # Load the CSV file into Pandas DataFrame
  df = pd.read_csv(CSV_PATH)
  # Save the DataFrame as an Excel file
  df.to_excel(EXCEL_PATH, index=False)
  print(f'Converted PDF file "{pdf_file_path}" to Excel file "{EXCEL_PATH}"')
  return EXCEL_PATH

def image_to_excel(image_file_path):
  # file name and paths
  EXCEL_FILE_NAME = f"image_to_excel_{uuid.uuid4()}.xlsx"
  EXCEL_PATH = os.path.join(STATIC_DIR, EXCEL_FILE_NAME)
  # Load the image file
  image = Image.open(image_file_path)
  # Convert the image to text using pytesseract
  text = pytesseract.image_to_string(image)
  # Split the text into rows and columns
  rows = text.split('\n')
  # cols = [row.split() for row in rows]
  cols = [row.split(',') for row in rows]
  # Create a new Excel workbook and select the active worksheet
  workbook = Workbook()
  worksheet = workbook.active
  # Write the data to the worksheet
  for row_index, row in enumerate(cols):
    for col_index, cell_value in enumerate(row):
      try: worksheet.cell(row=row_index+1, column=col_index+1, value=cell_value)
      except: pass
  # Save the Excel file
  workbook.save(EXCEL_PATH)
  print(f'Converted image file "{image_file_path}" to Excel file "{EXCEL_PATH}"')
  return EXCEL_PATH

def folder_to_zip(file_path):
  ZIP_FILE_NAME = f"zip_{uuid.uuid4()}.zip"
  ZIP_PATH = os.path.join(STATIC_DIR, ZIP_FILE_NAME)
  print('file excel_folder.zip...')
  cmd=f"zip -r {ZIP_PATH} {str(file_path)}"
  p1 = subprocess.Popen(cmd, shell=True)
  p1.wait()
  print('download file excel_folder.zip')
  return ZIP_PATH

def create_folder():
  # static folder 
  if not os.path.isdir("static"):
    os.mkdir("static")

def draw_bounding_box(file_path):
  # Easy OCR English words reader
  reader = easyocr.Reader(['en'], gpu=False)
  # read image
  img = cv2.imread(file_path)
  # resize image
  img = cv2.resize(img, (0, 0), fx = 0.6, fy = 0.6)
  # read text from image
  result = reader.readtext(img)
  detected_words = {word[1]:round(word[2]*100,2) for word in result}
  # print(f"result : {detected_words}")
  # draw bounding box
  spacer = 100
  font = cv2.FONT_HERSHEY_SIMPLEX
  for detection in result: 
      top_left = tuple(detection[0][0])
      bottom_right = tuple(detection[0][2])
      text = detection[1]
      img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),1)
      img = cv2.putText(img,text,(20,spacer), font, 0.5,(0,255,0),1,cv2.LINE_AA)
      spacer+=15
  # Filename
  output_filename = os.path.join("static", f"img_{uuid.uuid4()}.jpg")
  # Using cv2.imwrite() method, Saving the image
  cv2.imwrite(output_filename, img)
  print(f'\nConverted image file "{file_path}" to ploated bounding box "{output_filename}". \nSuccessfully saved')
  return output_filename, detected_words

def convert_to_excel(file_path):
  # Determine the file type
  if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
    output_filename, detected_words = draw_bounding_box(file_path)
    excel_file_path = image_to_excel(file_path)
    zip_file_path = folder_to_zip(excel_file_path)
    return {"input_image":file_path, "display_image":output_filename, "detected_words":detected_words, "download_excel":zip_file_path}
  elif file_path.lower().endswith('.pdf'):
    image_file_path = pdf_to_image(file_path)
    output_filename, detected_words = draw_bounding_box(image_file_path)
    # excel_file_path = image_to_excel(image_file_path)
    excel_file_path = pdf_to_excel(file_path)
    zip_file_path = folder_to_zip(excel_file_path)
    return {"input_image":image_file_path, "display_image":output_filename, "detected_words":detected_words, "download_excel":zip_file_path}
  else:
    print("Unsupported file format.")    
    