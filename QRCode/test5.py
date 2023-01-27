# import pywhatkit as pw
# import cv2

# txt = """Groundwater recharge or deep drainage or deep percolation is a hydrologic process, where water moves downward from surface water to groundwater. Recharge is the primary method through which water enters an aquifer.
#     Groundwater recharge can be defined as water added to the aquifer through the unsaturated zone after infiltration and percolation following any storm rainfall event.
#     Recharge can help move excess salts that accumulate in the root zone to deeper soil layers, or into the groundwater system. Tree roots increase water saturation into groundwater reducing water runoff.
# """

# # ex. 1
# # pw.text_to_handwriting(txt)

# # ex. 2
# pw.text_to_handwriting(txt, "demo1.png", [138,0,0])

# img = cv2.imread("demo1.png")
# cv2.imshow("Text to Handwriting", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print("END")



import qrcode as qr

txt = """Groundwater recharge or deep drainage or deep percolation is a hydrologic process, where water moves downward from surface water to groundwater. Recharge is the primary method through which water enters an aquifer.
    Groundwater recharge can be defined as water added to the aquifer through the unsaturated zone after infiltration and percolation following any storm rainfall event.
    Recharge can help move excess salts that accumulate in the root zone to deeper soil layers, or into the groundwater system. Tree roots increase water saturation into groundwater reducing water runoff.
"""

# # basic
# img = qr.make(txt)
# img.save("test_qr.png")

# advance
from PIL import Image

var_qr = qr.QRCode(version=1, error_correction=qr.ERROR_CORRECT_H, box_size=20, border=4)

var_qr.add_data(txt)
var_qr.make(fit=True)

img = var_qr.make_image(fill_color="red", back_color="green")
img.save("test_qr_adv.png")

