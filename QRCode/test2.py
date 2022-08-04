from ctypes import pointer
import cv2

"""
Read the QR Code
"""

detector = cv2.QRCodeDetector()

img = cv2.imread("QR1.jpg")

data, bbox, straight_qrcode = detector.detectAndDecode(img)

print(data)