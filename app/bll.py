import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.api import (api_mawaqit_login_get_token, get_prayer_times_by_mosque,
                     initialize_session)
from app.app_types import IAppConfig
from app.caster import playFile
from app.helper import get_server_ip
from app.schedulers import set_schedulers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def adhan_play(salat: str, app_config: IAppConfig):
    ip_address, host_name = get_server_ip()

    logger.info(f"Server IP: {ip_address}")
    logger.info(f"Host Name: {host_name}")

    # Always use IP address for Chromecast (not hostname)
    ip = ip_address
    file_name = "fajr" if salat == "fajr" else "default"
    volume = 0.30 if salat == "fajr" else 0.30

    port = app_config.get("port", 3050)
    url = f"http://{ip}:{port}/play/{file_name}.mp3"

    logger.info(f"Playing {salat} adhan from URL: {url} at volume: {volume}")

    playFile(app_config, volume, url)


def adhan_task_schedule(app_scheduler: BackgroundScheduler, app_config: IAppConfig):
    session = initialize_session()

    username = app_config["mawaqit"]["username"]
    password = app_config["mawaqit"]["password"]
    mosque_uuid = app_config["mawaqit"]["mosque_uuid"]

    print(f"Debug - Username: {username}")
    print(f"Debug - Password: {'*' * len(password) if password else None}")
    print(f"Debug - Mosque UUID: {mosque_uuid}")

    if not username or not password or not mosque_uuid:
        print("ERROR: Missing Mawaqit configuration. Please check environment variables:")
        print(f"  MAWAQIT_USERNAME: {'✓' if username else '✗'}")
        print(f"  MAWAQIT_PASSWORD: {'✓' if password else '✗'}")
        print(f"  MAWAQIT_MOSQUE: {'✓' if mosque_uuid else '✗'}")
        return

    token = api_mawaqit_login_get_token(username, password, session)

    if token is None:
        print("ERROR: Failed to login to Mawaqit API. Check credentials.")
        return

    print("✓ Successfully logged in to Mawaqit API")
    times = get_prayer_times_by_mosque(mosque_uuid, token, session)

    if times is None:
        print(f"ERROR: Failed to get prayer times for mosque UUID: {mosque_uuid}")
        return

    print("✓ Successfully retrieved prayer times")
    set_schedulers(app_scheduler, app_config, times, adhan_play)
