from django.core.mail import send_mail
from emailservice.settings import EMAIL_HOST_USER

def sendEmail(title, text, address):
    print(f"Send: {str(title)[:10]} {str(text)[:10]} EMAIL HOST: {EMAIL_HOST_USER} ADDRESS:{address}")
    send_mail(
        title,
        text,
        EMAIL_HOST_USER,
        [address],
        fail_silently=False,
    )
