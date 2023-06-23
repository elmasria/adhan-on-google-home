from datetime import datetime

import pytz
from apscheduler.schedulers.background import BackgroundScheduler


def set_schedulers(scheduler: BackgroundScheduler, times, cb):
    tz = pytz.timezone("Europe/Amsterdam")

    for salat, time in times["todayTimes"].items():
        hour, minute = map(int, time.split(":"))
        run_time = tz.localize(
            datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        )
        scheduler.add_job(
            cb, "date", run_date=run_time, id=salat, kwargs={"salat": salat}
        )


def set_daily_schedulers(scheduler: BackgroundScheduler, cb):
    scheduler.add_job(
        cb, "cron", id="set_daily_schedulers", hour=0, minute=5, args=[scheduler]
    )
