from backend.celery import app
from celery.schedules import crontab
from main.services import log


@app.task
def send_weekly():
    log("=1=2=3=4=5=6=7=8=9=10=11=12=13=14=15=16=17=18=19============", 'i')


@app.task
def queue_to_booking():
    log("2222222222222222222222222222222222222222222222222222222222222", 'i')


@app.task
def send_weekly_new():
    log("============", 'i')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    log("++++++++++++++++++++++++++++++++++++", 'i')
    log("Начало выполнения периодической задачи", 'i')
    sender.add_periodic_task(10.0, send_weekly.s(), name='test_send_weekly')
    sender.add_periodic_task(5.0, queue_to_booking.s(), name='queue_to_booking')
