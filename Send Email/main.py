from email.message import EmailMessage
import ssl
import smtplib

email_sender = "mungekarkiran05@gmail.com"
email_password = "byzvpuvtiiqztaqm" # app password for device

email_receiver = "mungekarkiran05@gmail.com"

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

