from apscheduler.schedulers.background import BackgroundScheduler

from app.api import (
    api_mawaqit_login_get_token,
    get_prayer_times_by_mosque,
    initialize_session,
)
from app.app_types import IAppConfig
from app.caster import playFile
from app.helper import get_server_ip
from app.schedulers import set_schedulers


def adhan_play(salat: str, app_config: IAppConfig):
    ip_address, host_name = get_server_ip()
    ip = host_name if ip_address == "127.0.0.1" else ip_address
    file_name = "fajr" if salat == "fajr" else "default"
    url = f"http://{ip}:5000/play/{file_name}.mp3"

    playFile(app_config, 0.45, url)


def adhan_task_schedule(app_scheduler: BackgroundScheduler, app_config: IAppConfig):
    session = initialize_session()

    username = app_config["mawaqit"]["username"]
    password = app_config["mawaqit"]["password"]
    mosque_uuid = app_config["mawaqit"]["mosque_uuid"]

    token = api_mawaqit_login_get_token(username, password, session)

    if token is None:
        print("Failed to login")
        return
    times = get_prayer_times_by_mosque(mosque_uuid, token, session)

    set_schedulers(app_scheduler, app_config, times, adhan_play)
