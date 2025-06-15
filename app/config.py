import os

from dotenv import load_dotenv

from app.app_types import IAppConfig

load_dotenv()


def get_app_config() -> IAppConfig:
    app_config: IAppConfig = {
        "mawaqit": {
            "username": os.getenv("MAWAQIT_USERNAME", None),
            "password": os.getenv("MAWAQIT_PASSWORD", None),
            "mosque_uuid": os.getenv("MAWAQIT_MOSQUE", None),
        },
        "device_name": os.getenv("DEVICE_NAME", None),
        "chromecast_ip": os.getenv("CHROMECAST_IP", None),
        "port": int(os.getenv("PORT", 5000)),
    }

    return app_config
