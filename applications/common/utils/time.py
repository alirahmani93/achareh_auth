from datetime import datetime
from django.utils.timezone import now

import datetime

from django.conf import settings

FORMAT_STR_YmdHM: str = "%Y-%m-%d %H:%M"


def get_now():
    return now()


def standard_response_datetime(time: datetime):
    return int(time.timestamp())


def standard_timestamp_response(input_time):
    return int(datetime.timestamp(input_time))


def get_now_time_stamp() -> int:
    return int(datetime.datetime.timestamp(now()))


def this_week():
    date = get_now()
    start_week = date - datetime.timedelta(date.weekday() + settings.START_WEEK_OFFSET)
    end_week = start_week + datetime.timedelta(
        days=7,
        hours=-start_week.hour,
        minutes=start_week.minute,
        seconds=start_week.second)
    return start_week, end_week


def spent_week() -> tuple:
    start_week, end_week = this_week()
    return start_week, get_now()


def spent_week_days() -> list:
    start_week, now = spent_week()
    week_offset = now.day - start_week.day
    return [(now - datetime.timedelta(days=-day)).date for day in range(week_offset.day)]


def standard_date_time_response(time: datetime):
    return time.strftime(FORMAT_STR_YmdHM)
