import os

from dotenv import load_dotenv

from app.app_types import IAppConfig

load_dotenv()


def get_app_config() -> IAppConfig:
    app_config: IAppConfig = {
        "mawaqit": {
            "username": os.getenv("MAWAQIT_USERNAME", None),
            "password": os.getenv("MAWAQIT_PASSWORD", None),
            "mosque_uuid": "653f569e-f6f1-4931-b61b-a8bfce5faeb5",
        },
        "device_name": "Kitchen display",
    }

    return app_config
