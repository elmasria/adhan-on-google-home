from datetime import datetime
from unittest.mock import MagicMock

import pytest
from apscheduler.schedulers.background import BackgroundScheduler

from app.schedulers import setSchedulers


@pytest.fixture
def times():
    return {
        "todayTimes": {
            "asr": "18:04",
            "dhuhr": "13:44",
            "fajr": "03:42",
            "isha": "23:43",
            "jumua": "14:00",
            "maghrib": "22:00",
            "shuruq": "05:22",
        }
    }


@pytest.fixture
def cb():
    return MagicMock()


@pytest.fixture
def scheduler():
    return BackgroundScheduler()


def test_setSchedulers(times, cb, scheduler):
    current_hour, current_minute = map(int, datetime.now().strftime("%H:%M").split(":"))

    future_times = 0
    for salat, time in times["todayTimes"].items():
        hour, minute = map(int, time.split(":"))
        is_a_future_time = hour > current_hour or (
            hour == current_hour and minute > current_minute
        )
        if is_a_future_time:
            future_times += 1

    setSchedulers(scheduler, times, cb)

    assert len(scheduler.get_jobs()) == future_times
