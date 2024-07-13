import cv2
import easyocr
from matplotlib import pyplot as plt

def ocr_and_face_detection(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR on the image using EasyOCR
    reader = easyocr.Reader(['en'])
    ocr_result = reader.readtext(gray)

    # Extract text from OCR result
    text = "\n".join([item[1] for item in ocr_result])
    print("OCR Result:")
    print(text)

    # Load OpenCV pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # # Use matplotlib to display the image
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.title('Image with Face Detection')
    # plt.axis('off')
    # plt.show()

    # Save the image with face detections
    cv2.imwrite('output_image.png', image)

    return text, faces

if __name__ == '__main__':
    image_path = 'images/id_card_cp1.png'  # Replace with your ID card image path
    ocr_text, detected_faces = ocr_and_face_detection(image_path)

    # Print detected faces
    print("Detected faces:")
    for i, (x, y, w, h) in enumerate(detected_faces):
        print(f"Face {i+1}: x={x}, y={y}, w={w}, h={h}")
