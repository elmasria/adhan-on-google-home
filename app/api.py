import json
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

from app.app_types import IPrayerTimes


def initialize_session() -> requests.Session:
    return requests.Session()


def api_mawaqit_login_get_token(
    username: str, password: str, session: requests.Session
) -> Optional[str]:
    LOGIN_URL = "https://mawaqit.net/api/2.0/me"
    response = session.get(LOGIN_URL, auth=HTTPBasicAuth(username, password))

    if response.status_code != 200:
        return None

    data = response.text
    token = json.loads(data)["apiAccessToken"]
    return token


def get_prayer_times_by_mosque(
    uuid: str, token: str, session: requests.Session
) -> Optional[IPrayerTimes]:
    try:
        headers = {
            "Accept": "application/json",
            "Api-Access-Token": format(token),
        }
        response = session.get(
            f"https://mawaqit.net/api/2.0/mosque/{uuid}/prayer-times",
            headers=headers,
            params={"calendar": "true"},
        )
        if response.status_code == 200:
            data = response.json()
            salat_list = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
            today_times = {
                salat: time for salat, time in zip(salat_list, data["times"])
            }
            # today_times["jumua"] = data["jumua"]
            # today_times["shuruq"] = data["shuruq"]

            return {"todayTimes": today_times}
        return None
    except Exception as error:
        print(f"An error occurred: {error}")
        return None
