from datetime import datetime

# date from second to local hour
def to_local_hour(date_in_second, timezone_in_second):
    return datetime.fromtimestamp(date_in_second + timezone_in_second).time()

# timezone from second to hour
def timezone_to_hour(timezone_in_second):
    return int(timezone_in_second / 3600)

# date from iso format to hour
def format_iso_to_hour(date_in_iso_format):
    return datetime.fromisoformat(date_in_iso_format).time()