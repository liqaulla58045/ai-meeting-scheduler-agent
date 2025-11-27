from datetime import datetime


def create_google_calendar_event(meeting_data: dict) -> dict:
    """
    Stub function simulating Google Calendar integration.

    This does NOT call real Google APIs. It just returns a fake event structure
    so the UI can show a success message.

    Expected keys in meeting_data:
    - title
    - start_time
    - end_time
    - participants
    - recurrence_type (optional)
    - recurrence_until (optional)
    """

    title = meeting_data.get("title", "Meeting")
    start = meeting_data.get("start_time")
    end = meeting_data.get("end_time")

    # Fake event id + link
    event_id = f"fake-{int(datetime.utcnow().timestamp())}"
    event_link = f"https://calendar.google.com/calendar/r/eventedit/{event_id}"

    return {
        "event_id": event_id,
        "event_link": event_link,
        "title": title,
        "start": start.isoformat() if start else None,
        "end": end.isoformat() if end else None,
    }
