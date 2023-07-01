import time

import pychromecast

from app.app_types import IAppConfig


def getDeviceByName(friendly_name):
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=[friendly_name]
    )

    if chromecasts is None:
        return False

    cast_device = chromecasts[0]

    cast_device.wait()
    return cast_device, browser


def close_running_app(device):
    if not device.is_idle:
        print("Killing current running app")
        device.quit_app()
        t = 5
        while device.status.app_id is not None and t > 0:
            time.sleep(0.1)
            t = t - 0.1


def playFile(app_config: IAppConfig, volume, file_url, file_type="audio/mp3"):
    device, browser = getDeviceByName(app_config.get("device_name"))
    close_running_app(device)

    device.set_volume(volume)
    time.sleep(1)

    device.play_media(file_url, file_type)
    time.sleep(10)

    browser.stop_discovery()
