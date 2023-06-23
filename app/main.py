from apscheduler.schedulers.background import BackgroundScheduler
from bll import adhan_task_schedule
from flask_app import init_app
from schedulers import set_daily_schedulers

app_scheduler = BackgroundScheduler()
app = init_app(app_scheduler)

set_daily_schedulers(app_scheduler, adhan_task_schedule)
adhan_task_schedule(app_scheduler)

app_scheduler.start()

app.run(debug=True, host="0.0.0.0")
