from django.core.mail import send_mail
from emailservice.settings import EMAIL_HOST_USER
import logging
import datetime


def sendEmail(title, text, address):
    print(f"Send: {str(title)[:10]} {str(text)[:10]} EMAIL HOST: {EMAIL_HOST_USER} ADDRESS:{address}")
    send_mail(
        title,
        text,
        EMAIL_HOST_USER,
        [address],
        fail_silently=False,
    )


def log(string, log_type="w"):
    _ = f"{str(datetime.datetime.now())[:-7]} {string}"
    if log_type == "d":
        logging.debug(_)
    elif log_type == "i":
        logging.info(_)
    elif log_type == "w":
        logging.warning(_)
    elif log_type == "e":
        logging.error(_)
    elif log_type == "c":
        logging.critical(_)
    else:
        logging.debug(_)
