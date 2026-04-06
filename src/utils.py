import sys
from datetime import datetime, timedelta, timezone
import requests
import logging


def tsConv(unix_timestamp, returnUntil=False):
    # Convert UNIX timestamp to timezone-aware datetime object in UTC
    dt_utc = datetime.fromtimestamp(unix_timestamp / 1000.0, tz=timezone.utc)

    # Get the local timezone
    local_tz = datetime.now().astimezone().tzinfo

    # Convert UTC datetime to local datetime
    dt_local = dt_utc.astimezone(local_tz)

    # Format the local datetime in "DD/MM/YYYY at HH:MM AM/PM" format
    formatted_date = dt_local.strftime("%d/%m/%Y at %I:%M %p")

    dates = [formatted_date]

    if returnUntil:
        # Calculate the time difference between now and the timestamp date
        now_local = datetime.now().astimezone(local_tz)
        time_difference = dt_local - now_local

        if time_difference <= timedelta(days=1):
            hours_left = int(time_difference.total_seconds() // 3600)
            dates.append(f"in {hours_left} hours")
        else:
            days_left = time_difference.days
            dates.append(f"in {days_left} days")

    return dates


def check_internet_connection():
    try:
        response = requests.get("https://google.com/", timeout=5)
        if response.status_code == 200:
            logging.info("Internet connection is available.")
    except requests.RequestException as e:
        logging.error("Internet Connection Error — No internet connection available. Exiting...")
        sys.exit(1)
