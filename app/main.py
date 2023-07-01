from apscheduler.schedulers.background import BackgroundScheduler

from app.app_types import IAppConfig
from app.bll import adhan_task_schedule
from app.config import get_app_config
from app.flask_app import init_app
from app.schedulers import set_daily_schedulers

app_config: IAppConfig = get_app_config()

app_scheduler = BackgroundScheduler()

app = init_app(app_scheduler, app_config)

set_daily_schedulers(app_scheduler, app_config, adhan_task_schedule)
adhan_task_schedule(app_scheduler, app_config)

app_scheduler.start()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
