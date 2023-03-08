from datetime import datetime, timedelta


def calculate_time_delta(time1, time2):
    """Calculates time difference between two given timestamps in specific format
    :param time1 start timestamp
    :param time2 end timestamp
    :returns timedelta or None
    """
    try:
        delta = datetime.fromisoformat(time2) - datetime.fromisoformat(time1)
        return delta
    except ValueError:
        return None


def validate_layover(delta):
    """Checks if layover time (between one flight's arrival and another's departure)
    is valid, i.e being from 1 to 6 hours
    :param delta: timestamp of calculated time-delta
    :returns boolean or None"""
    try:
        return timedelta(hours=1.0) <= delta <= timedelta(hours=6.0)
    except TypeError:
        return None
