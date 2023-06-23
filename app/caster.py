import pychromecast


def getDeviceByName(friendly_name):
    chromecasts, _ = pychromecast.get_chromecasts()
    cast_device = next(
        (cc for cc in chromecasts if cc.cast_info.friendly_name == friendly_name), None
    )

    if cast_device is None:
        return False

    cast_device.wait()
    return cast_device


def playFile(device, volume, file_url, file_type="audio/mp3"):
    device.set_volume(volume)

    mc = device.media_controller
    mc.play_media(file_url, file_type)
    mc.block_until_active()
