import logging
from datetime import datetime, timezone, timedelta

def parse_date(date_str):
    if date_str:
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
            target_tz = timezone(timedelta(hours=6))
            converted = dt.astimezone(target_tz).replace(tzinfo=None)
            return converted
        except ValueError:
            logging.error(f"Warning: Invalid date format for {date_str}")
            return None
    return None