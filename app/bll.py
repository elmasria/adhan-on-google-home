from api import (
    api_mawaqit_login_get_token,
    get_prayer_times_by_mosque,
    initialize_session,
)
from apscheduler.schedulers.background import BackgroundScheduler
from caster import getDeviceByName, playFile
from schedulers import set_schedulers


def adhan_play(salat: str):
    device = getDeviceByName("Office speaker")
    playFile(device, 0.4, "")


def adhan_task_schedule(app_scheduler: BackgroundScheduler):
    session = initialize_session()
    token = api_mawaqit_login_get_token("", "", session)
    times = get_prayer_times_by_mosque(
        "653f569e-f6f1-4931-b61b-a8bfce5faeb5", token, session
    )

    set_schedulers(app_scheduler, times, adhan_play)
