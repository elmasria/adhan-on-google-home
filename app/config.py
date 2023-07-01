import os

from dotenv import load_dotenv

from app.app_types import IAppConfig

load_dotenv()


def get_app_config() -> IAppConfig:
    app_config: IAppConfig = {
        "mawaqit": {
            "username": os.getenv("MAWAQIT_USERNAME", None),
            "password": os.getenv("MAWAQIT_PASSWORD", None),
            "mosque_uuid": os.getenv("DEVICE_NAME", None),
        },
        "device_name": os.getenv("MAWAQIT_MOSQUE", None),
    }

    return app_config
