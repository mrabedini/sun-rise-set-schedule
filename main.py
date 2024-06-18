# main.py

from datetime import datetime, timedelta
from decouple import config
from utils import authenticate_google, get_sunset_time, create_event
from googleapiclient.discovery import build


def main():
    # Read values from .env file
    timezone = config("MY_TIMEZONE")
    lat = config("MY_CITY_LAT")
    sleep_time = config("MY_SLEEP_TIME")
    lng = config("MY_CITY_LNG")
    credentials_path = config("GOOGLE_API_CREDENTIALS")

    # Authenticate with Google
    creds = authenticate_google(credentials_path)
    service = build("calendar", "v3", credentials=creds)

    # Schedule events for the next 7 days
    today = datetime.now().date()
    for day_offset in range(7):
        current_date = today + timedelta(days=day_offset)
        sunset_time_str = get_sunset_time(lat, lng, current_date, timezone)

        # Parse sunset time
        sunset_time = datetime.strptime(sunset_time_str, "%I:%M:%S %p")
        sunset_time = datetime.combine(current_date, sunset_time.time())

        # Define start and end times for the event
        start_time = sunset_time
        end_time = datetime.combine(
            current_date, datetime.strptime(sleep_time, "%H:%M:%S").time()
        )

        # Convert times to ISO format
        start_time_iso = start_time.isoformat()
        end_time_iso = end_time.isoformat()

        # Create the event on Google Calendar
        create_event(service, start_time_iso, end_time_iso, timezone)


if __name__ == "__main__":
    main()
