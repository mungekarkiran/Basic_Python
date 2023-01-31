# https://www.youtube.com/watch?v=QKeywJ4WOfM
# https://www.youtube.com/watch?v=JLLE11Eo4fc
# https://www.youtube.com/watch?v=66ZtJI-06bQ
# https://www.youtube.com/watch?v=DTOXB1ApzRo
# https://www.youtube.com/watch?v=Cp37ORZhJcE
# https://www.youtube.com/watch?v=g_j6ILT-X0k

from email.message import EmailMessage
import ssl
import smtplib

email_sender = "m5@gmail.com"
email_password = "byzvpuvtiiqztaqm" # app password for device

email_receiver = "m5@gmail.com"

subject = "Dont forget to add subject"
body = """
    Hello Body
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

