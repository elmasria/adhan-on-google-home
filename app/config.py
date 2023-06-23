import os

from app_types import IAppConfig


def get_app_config() -> IAppConfig:
    app_config: IAppConfig = {
        "mawaqit": {
            "username": os.getenv("MAWAQIT_USERNAME", None),
            "password": os.getenv("MAWAQIT_PASSWORD", None),
            "mosque_uuid": "653f569e-f6f1-4931-b61b-a8bfce5faeb5",
        }
    }

    return app_config
