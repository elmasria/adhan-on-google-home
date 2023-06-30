import pychromecast


def getDeviceByName(friendly_name):
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=[friendly_name]
    )

    if chromecasts is None:
        return False

    cast_device = chromecasts[0]

    cast_device.wait()
    return cast_device, browser


def playFile(device, volume, file_url, file_type="audio/mp3"):
    device.set_volume(volume)
    device.play_media(file_url, file_type)
