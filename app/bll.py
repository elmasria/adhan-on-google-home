import time

from apscheduler.schedulers.background import BackgroundScheduler

from app.api import (
    api_mawaqit_login_get_token,
    get_prayer_times_by_mosque,
    initialize_session,
)
from app.app_types import IAppConfig
from app.caster import getDeviceByName, playFile
from app.helper import get_server_ip
from app.schedulers import set_schedulers


def adhan_play(salat: str, app_config: IAppConfig):
    device, browser = getDeviceByName(app_config.get("device_name"))
    ip = get_server_ip()

    file_name = "fajr" if salat == "fajr" else "default"
    url = f"http://{ip}:5000/play/{file_name}.mp3"

    if not device.is_idle:
        print("Killing current running app")
        device.quit_app()
        t = 5
        while device.status.app_id is not None and t > 0:
            time.sleep(0.1)
            t = t - 0.1

    playFile(device, 0.45, url)
    time.sleep(10)
    browser.stop_discovery()


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
