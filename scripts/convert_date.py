from datetime import datetime

def to_local_hour(date_in_second, timezone_in_second):
    return datetime.fromtimestamp(date_in_second + timezone_in_second).time()

def timezone_to_hour(timezone_in_second):
    return int(timezone_in_second / 3600)

def format_iso_to_hour(date_in_iso_format):
    return datetime.fromisoformat(date_in_iso_format).time()