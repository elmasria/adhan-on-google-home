import logging
import time

import pychromecast

from app.app_types import IAppConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def getDeviceByName(friendly_name):
    logger.info(f"Starting discovery for device: {friendly_name}")

    # Method 1: Try standard discovery with timeout
    logger.info("Method 1: Trying standard discovery...")
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=[friendly_name],
        timeout=10  # Add timeout
    )
    logger.info(f"Found {len(chromecasts)} devices with targeted search")

    if chromecasts and len(chromecasts) > 0:
        cast_device = chromecasts[0]
        cast_device.wait()
        return cast_device, browser

    # Method 2: Try discovering all chromecasts with longer timeout
    logger.info("Method 2: Discovering all chromecasts...")
    try:
        services, browser = pychromecast.discovery.discover_chromecasts(timeout=15)
        logger.info(f"Discovery found {len(services)} total services")

        # List all found devices for debugging
        all_devices = [cc.friendly_name for cc in services]
        logger.info(f"All discovered devices: {all_devices}")

        # Look for exact match
        matching_devices = [cc for cc in services if cc.friendly_name == friendly_name]

        if matching_devices:
            logger.info(f"Found matching device: {matching_devices[0].friendly_name}")
            cast_device = pychromecast.get_chromecast_from_service(matching_devices[0], browser)
            cast_device.wait()
            return cast_device, browser

        # Try case-insensitive match
        case_insensitive_matches = [
            cc for cc in services
            if cc.friendly_name.lower() == friendly_name.lower()
        ]

        if case_insensitive_matches:
            logger.info(f"Found case-insensitive match: {case_insensitive_matches[0].friendly_name}")
            cast_device = pychromecast.get_chromecast_from_service(case_insensitive_matches[0], browser)
            cast_device.wait()
            return cast_device, browser

    except Exception as e:
        logger.error(f"Error during discovery: {e}")

    # Method 3: Try get_chromecasts (discovers all devices)
    logger.info("Method 3: Trying get_chromecasts...")
    try:
        chromecasts, browser = pychromecast.get_chromecasts(timeout=15)
        logger.info(f"get_chromecasts found {len(chromecasts)} devices")

        all_names = [cc.name for cc in chromecasts]
        logger.info(f"Device names from get_chromecasts: {all_names}")

        for cc in chromecasts:
            if cc.name == friendly_name or cc.name.lower() == friendly_name.lower():
                logger.info(f"Found match via get_chromecasts: {cc.name}")
                cc.wait()
                return cc, browser

    except Exception as e:
        logger.error(f"Error with get_chromecasts: {e}")

    logger.error(f"No Chromecast device found with name: {friendly_name}")
    return False, browser


def close_running_app(device):
    if not device.is_idle:
        logger.info("Killing current running app")
        device.quit_app()
        t = 5
        while device.status.app_id is not None and t > 0:
            time.sleep(0.1)
            t = t - 0.1


def playFile(app_config: IAppConfig, volume, file_url, file_type="audio/mp3"):
    # Try manual IP first if provided, but only if device name matches
    chromecast_ip = app_config.get("chromecast_ip")
    device_name = app_config.get("device_name")
    if chromecast_ip and chromecast_ip != "FIND_OFFICE_SPEAKER_IP":
        logger.info(f"Trying manual IP connection to {chromecast_ip}")
        try:
            # Use discovery with known IP address - this is the recommended approach
            logger.info(f"Discovering Chromecast at IP: {chromecast_ip}")
            chromecasts, browser = pychromecast.get_chromecasts(known_hosts=[chromecast_ip])
            if chromecasts:
                # IMPORTANT: known_hosts doesn't filter! We must filter by actual IP
                devices_at_ip = [cc for cc in chromecasts if cc.cast_info.host == chromecast_ip]
                logger.info(f"Found {len(devices_at_ip)} devices at IP {chromecast_ip}: {[cc.name for cc in devices_at_ip]}")

                if not devices_at_ip:
                    logger.warning(f"No devices actually at IP {chromecast_ip}. Falling back to name discovery.")
                    result = getDeviceByName(device_name)
                    if result[0] is False:
                        logger.error("Failed to find correct Chromecast device, cannot play file")
                        result[1].stop_discovery()
                        return False
                    device, browser = result
                elif device_name:
                    # Filter by device name from devices at the IP
                    matching_devices = [cc for cc in devices_at_ip if cc.name == device_name]
                    if matching_devices:
                        device = matching_devices[0]
                        logger.info(f"Found matching Chromecast: {device.name} at {chromecast_ip}")
                    else:
                        # Try case-insensitive match
                        case_insensitive_matches = [cc for cc in devices_at_ip if cc.name.lower() == device_name.lower()]
                        if case_insensitive_matches:
                            device = case_insensitive_matches[0]
                            logger.info(f"Found case-insensitive match: {device.name} at {chromecast_ip}")
                        else:
                            logger.warning(f"No device named '{device_name}' at IP {chromecast_ip}. Available at this IP: {[cc.name for cc in devices_at_ip]}. Falling back to name discovery.")
                            result = getDeviceByName(device_name)
                            if result[0] is False:
                                logger.error("Failed to find correct Chromecast device, cannot play file")
                                result[1].stop_discovery()
                                return False
                            device, browser = result
                else:
                    # No device name specified, use first device at the IP
                    device = devices_at_ip[0]
                    logger.info(f"Found Chromecast: {device.name} at {chromecast_ip}")

                # Wait for device to be fully connected
                device.wait(timeout=10)
                logger.info(f"Successfully connected to {device.name} via manual IP")
            else:
                logger.error(f"No Chromecast found at IP {chromecast_ip}")
                # Fall back to discovery by name
                result = getDeviceByName(app_config.get("device_name"))
                if result[0] is False:
                    logger.error("Failed to find Chromecast device, cannot play file")
                    result[1].stop_discovery()
                    return False
                device, browser = result
        except Exception as e:
            logger.error(f"Manual IP connection failed: {e}")
            # Fall back to discovery
            result = getDeviceByName(app_config.get("device_name"))
            if result[0] is False:
                logger.error("Failed to find Chromecast device, cannot play file")
                result[1].stop_discovery()
                return False
            device, browser = result
    else:
        # Use normal discovery
        result = getDeviceByName(app_config.get("device_name"))
        if result[0] is False:
            logger.error("Failed to find Chromecast device, cannot play file")
            result[1].stop_discovery()
            return False
        device, browser = result
    close_running_app(device)

    device.set_volume(volume)
    time.sleep(1)

    device.play_media(file_url, file_type)
    time.sleep(10)

    browser.stop_discovery()
    return True
