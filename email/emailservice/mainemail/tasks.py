from emailservice.celery import app
from celery.schedules import crontab
from mainemail.services import sendEmail
from mainemail.services import log


@app.task
def send_verification_email(user_id):
    try:
        sendEmail("TEST", f"+ celery celery{user_id}", "kristal.as@phystech.edu")
    except Exception as e:
        print(e)


@app.task
def send_task_email(email_address: str, email_text: str, email_title: str):
    try:
        sendEmail(email_title, email_text, email_address)
    except Exception as e:
        print(e)


@app.task
def send_weekly():
    try:
        sendEmail("TEST", "периодично периодично", "kristal.as@phystech.edu")
        return 1
    except Exception as e:
        print(e)
        return 0


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    log("Начало выполнения периодической задачи", 'i')
    sender.add_periodic_task(50.0, send_weekly.s(), name='test_send_weekly')
