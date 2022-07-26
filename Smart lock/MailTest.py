#working
# https://www.instructables.com/id/Send-Email-Using-Python/
# https://gist.github.com/nickoala/569a9d191d088d82a5ef5c03c0690a02
# thanks god......
import smtplib
from email.mime.text import MIMEText

smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
smtp_ssl_port = 465 #587 #465
#'mungekarkiran05@gmail.com', 'shubhamneve2015@gmail.com','panpatilabhijeet66@gmail.com'
username = 'id'
password = 'pass'
sender = 'shubhamneve2015@gmail.com'
targets = ['panpatilabhijeet66@gmail.com',
           'mungekarkiran05@gmail.com',
           'shubhamneve2015@gmail.com']

msg = MIMEText('Hi, how are you today? Someone is trying to open your door now')
#msg = MIMEText('sala panawati gela aani lib install zali..')
msg['Subject'] = 'Alert'
msg['From'] = sender
msg['To'] = ', '.join(targets)

while(1):
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()
