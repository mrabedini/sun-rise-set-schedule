# utils.py

import requests
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow

# Setup the Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def authenticate_google(credentials_path):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds


def get_sunset_time(lat, lng, date, timezone):
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}&tzid={timezone}"
    response = requests.get(url)
    data = response.json()
    return data["results"]["sunset"]


def create_event(service, start_time, end_time, timezone):
    event = {
        "summary": "Me-Time",
        "start": {
            "dateTime": start_time,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone,
        },
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
