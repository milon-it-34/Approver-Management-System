import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(from_email, to_email, subject, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'milon.ict.bd34@gmail.com'
    smtp_password = 'jcer brqc lgqt lpcx'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    server.sendmail(from_email, to_email, msg.as_string())

    server.quit()
