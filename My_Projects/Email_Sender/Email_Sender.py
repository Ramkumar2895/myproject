import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

inp = open('input.txt','r',encoding = 'utf-8')
for i in inp:
    mailId, myfileName = i.split("\t")
    
    email_user = "ramkumar1995.rk94@gmail.com"
    my_password = "password"

    send_to = mailId.strip()
    subject = "Subject"

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = send_to
    msg['subject'] = subject

    body = "Hi its me ram....!"

    msg.attach(MIMEText(body,'Plain'))

    fileName = myfileName.strip()
    attachment = open(fileName,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename = "+fileName)
    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo
    server.login(email_user,my_password)

    server.sendmail(email_user,send_to,text)
    server.quit()


