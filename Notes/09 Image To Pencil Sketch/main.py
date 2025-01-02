# Convert an Image to Pencil Sketch
# pip install opencv-python

import cv2

def convert_to_pencil_sketch(image_path, output_path="pencil_sketch.jpg"):
    # Read the original image
    image = cv2.imread(image_path)
    
    # Check if the image is loaded successfully
    if image is None:
        print("Error: Unable to load image. Please check the file path.")
        return

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invert the grayscale image
    inverted_gray_image = 255 - gray_image
    
    # Apply Gaussian blur to the inverted image
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), sigmaX=0, sigmaY=0)
    
    # Invert the blurred image
    inverted_blurred_image = 255 - blurred_image
    
    # Create the pencil sketch by dividing the grayscale image by the inverted blurred image
    pencil_sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
    
    # Save the pencil sketch to a file
    cv2.imwrite(output_path, pencil_sketch)
    print(f"Pencil sketch saved as: {output_path}")
    
    # Display the original image and pencil sketch (optional)
    cv2.imshow("Original Image", image)
    cv2.imshow("Pencil Sketch", pencil_sketch)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "image2.png" # "input_image.jpg"  # Replace with your image path
convert_to_pencil_sketch(image_path)
