from api import (
    api_mawaqit_login_get_token,
    get_prayer_times_by_mosque,
    initialize_session,
)
from app_types import IAppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from caster import getDeviceByName, playFile
from helper import get_server_ip
from schedulers import set_schedulers


def adhan_play(salat: str):
    device = getDeviceByName("Office speaker")
    ip = get_server_ip()

    file_name = "fajr" if salat == "fajr" else "default"
    url = f"http://{ip}:5000/play/{file_name}.mp3"

    playFile(device, 0.4, url)


def adhan_task_schedule(app_scheduler: BackgroundScheduler, app_config: IAppConfig):
    session = initialize_session()

    username = app_config["mawaqit"]["username"]
    password = app_config["mawaqit"]["password"]
    mosque_uuid = app_config["mawaqit"]["mosque_uuid"]

    token = api_mawaqit_login_get_token(username, password, session)

    times = get_prayer_times_by_mosque(mosque_uuid, token, session)

    set_schedulers(app_scheduler, times, adhan_play)
