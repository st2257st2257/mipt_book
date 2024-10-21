from backend.celery import app
from celery.schedules import crontab
from main.services import log, send_email, get_timetable, update_audience, update_audience_day


@app.task
def send_weekly():
    log("=1=2=3=4=5=6=7=8=9=10=11=12=13=14=15=16=17=18=19============", 'i')


@app.task
def queue_to_booking():
    log("START SENDING", 'i')
    try:
        log(str(get_timetable()), "i")
    except Exception as e:
        log(e, "e")
        log("333333333333333333333333333333333333333333333333333333333", 'i')


@app.task
def update_audience_regular(week_day):
    # Обновление аудитории к заданномк времени
    log(f"REGULAR UPDATE: +++ === +++ ={week_day}= +++ === +++", 'i')
    update_audience(week_day)
    log(f"REGULAR UPDATE: 000 === 000 ={week_day}= 000 === 000", 'i')


@app.task
def update_week_day(day_index):
    # обновление актуальних бронирований к началу дня
    log(f"REGULAR UPDATE: --- === --- ={day_index}= --- === ---", 'i')
    update_audience_day(day_index)


@app.task
def send_weekly_new():
    log("============", 'i')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    log("++++++++++++++++++++++++++++++++++++", 'i')
    log("Начало выполнения периодической задачи", 'i')
    sender.add_periodic_task(10.0, send_weekly.s(), name='test_send_weekly')
    sender.add_periodic_task(5.0, queue_to_booking.s(), name='queue_to_booking')
    sender.add_periodic_task(5.0, update_audience_regular.s(), name='update_audience_regular')
    sender.add_periodic_task(5.0, update_week_day.s(), name='update_week_day')
