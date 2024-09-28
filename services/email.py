import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def get_date() -> str:
    return datetime.now().strftime('%d/%m/%Y')


class EmailMessageBuilder:
    def __init__(self, sender, recipient, subject, body):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.msg = MIMEMultipart()

    def create_message(self):
        self.msg['From'] = self.sender
        self.msg['To'] = self.recipient
        self.msg['Subject'] = self.subject
        self.msg.attach(MIMEText(self.body, 'plain'))
        return self.msg


class EmailAttachment:
    def __init__(self, filepath):
        self.filepath = filepath

    def attach(self, msg):
        if self.filepath and os.path.isfile(self.filepath):
            part = MIMEBase('application', 'octet-stream')

            with open(self.filepath, 'rb') as file:
                part.set_payload(file.read())

            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(self.filepath)}')
            msg.attach(part)


class SMTPSender:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send(self, msg):
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
        except Exception as e:
            print(f'Erro ao enviar e-mail: {e}')


class EmailService:
    def __init__(self, email_sender, sender):
        self.email_sender = email_sender
        self.sender = sender

    def send_email(self, body, subject, recipient, attachment_path=None):
        builder = EmailMessageBuilder(self.sender, recipient, subject, body)
        msg = builder.create_message()

        if attachment_path:
            attachment = EmailAttachment(attachment_path)
            attachment.attach(msg)

        self.email_sender.send(msg)


SMTP_SERVER = ''
SMTP_PORT = 587
USERNAME = ''
PASSWORD = ''

smtp_sender = SMTPSender(SMTP_SERVER, SMTP_PORT, USERNAME, PASSWORD)

email_service = EmailService(
    email_sender=smtp_sender,
    sender=USERNAME,
)
