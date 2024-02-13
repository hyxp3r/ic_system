import smtplib
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

from api.config import MailSettings


def send_verification_code(email: str, code: str):
    settings = MailSettings()

    env = Environment(loader=FileSystemLoader('api/templates/mail'))
    template = env.get_template('verify_mail.html')

    from_email = settings.from_email
    smtp_server = settings.smtp_server
    smtp_port = settings.smtp_port
    smtp_username = settings.smtp_username
    smtp_password = settings.smtp_password

    message = MIMEText(template.render(code=code), 'html')
    message['Subject'] = 'Код подтверждения'
    message['From'] = from_email
    message['To'] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, [email], message.as_string())
