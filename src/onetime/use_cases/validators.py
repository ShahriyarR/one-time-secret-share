import datetime


def is_expired(origin: datetime.datetime, expire_after: int) -> bool:
    current = datetime.datetime.now()
    time_delta = current - origin
    time_delta_in_hours = int(round(time_delta.total_seconds() / 3600, 0))
    return time_delta_in_hours > expire_after
