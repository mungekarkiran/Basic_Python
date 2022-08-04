import qrcode

"""
Make the QR Code
"""

img = qrcode.make("https://www.youtube.com/watch?v=Rs3GfkHRwXA")

img.save("QR1.jpg")