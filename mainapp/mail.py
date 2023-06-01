import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

login = 'gambam-community@yandex.ru'
password = 'Papagaga2024'


def send_email(to_addr, subject, text):
    msg = MIMEMultipart()
    msg['From'] =  login
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(
        MIMEText(text, 'plain')
    )

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo(login)
    server.login(login, password)
    server.auth_plain()
    server.send_message(msg)
    server.quit()

send_email(input(), input(), input())