from emailservice.celery import app
from celery.schedules import crontab
from mainemail.services import sendEmail

@app.task
def send_verification_email(user_id):
    try:
        sendEmail("TEST", f"celery celery{user_id}", "kristal.as@phystech.edu")
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
    sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)
    try:
        sendEmail("TEST", "периодично периодично", "kristal.as@phystech.edu")
    except Exception as e:
        print(e)

