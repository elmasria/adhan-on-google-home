from datetime import datetime

import pytz


def setSchedulers(scheduler, times, cb):
    tz = pytz.timezone("Europe/Amsterdam")

    for salat, time in times["todayTimes"].items():
        hour, minute = map(int, time.split(":"))
        run_time = tz.localize(
            datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        )
        scheduler.add_job(
            cb, "date", run_date=run_time, id=salat, kwargs={"salat": salat}
        )

    scheduler.start()
