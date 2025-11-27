from datetime import datetime, timedelta
from dateutil import parser as date_parser
import pytz
import re

IST = pytz.timezone("Asia/Kolkata")


def parse_meeting_request(user_input: str):
    """
    Offline/local parser for meeting extraction without external APIs.

    Extracts best-effort:
    - title
    - start_time
    - end_time
    - participants
    - recurrence_type: none/daily/weekly/monthly
    - recurrence_until: optional end date
    """

    text = user_input.strip()
    lower = text.lower()

    now = datetime.now(IST)
    start_time = now + timedelta(hours=1)
    duration_minutes = 30
    title = "Meeting"
    participants = ""

    recurrence_type = "none"
    recurrence_until = None

    # Duration: "30 minutes", "1 hour", "2 hrs"
    dur = re.search(r"(\d+)\s*(minute|min|hour|hr|hours|hrs)", lower)
    if dur:
        num = int(dur.group(1))
        unit = dur.group(2)
        if "hour" in unit or "hr" in unit:
            duration_minutes = num * 60
        else:
            duration_minutes = num

    # Date: today / tomorrow
    base_date = now
    if "tomorrow" in lower:
        base_date = now + timedelta(days=1)
    elif "today" in lower:
        base_date = now

    # Time: "4 pm", "11:30 am", "16:00"
    time_match = re.search(r"(\d{1,2}(:\d{2})?\s*(am|pm))", lower)
    parsed_time = None
    if time_match:
        try:
            parsed_time = date_parser.parse(time_match.group(1))
        except Exception:
            parsed_time = None

    if parsed_time:
        start_time = base_date.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=0,
            microsecond=0,
        )
    else:
        # If no explicit time, next full hour
        start_time = base_date.replace(
            minute=0, second=0, microsecond=0
        ) + timedelta(hours=1)

    # Participants: after "with"
    with_idx = lower.find("with")
    if with_idx != -1:
        participants = text[with_idx + len("with"):].strip()
        about_idx = participants.lower().find("about")
        if about_idx != -1:
            participants = participants[:about_idx].strip()

    # Title/topic: after "about"
    about_idx_full = lower.find("about")
    if about_idx_full != -1:
        title = text[about_idx_full + len("about"):].strip().capitalize() or "Meeting"
    else:
        title = text[:60] + ("..." if len(text) > 60 else "")

    # Recurrence: daily/weekly/monthly
    if "every day" in lower or "daily" in lower:
        recurrence_type = "daily"
    elif "every week" in lower or "weekly" in lower:
        recurrence_type = "weekly"
    elif "every month" in lower or "monthly" in lower:
        recurrence_type = "monthly"

    # Optional: "until <date>"
    m_until = re.search(r"until\s+([a-zA-Z0-9 ,/-]+)", lower)
    if m_until:
        try:
            dt = date_parser.parse(m_until.group(1), dayfirst=True)
            recurrence_until = IST.localize(dt)
        except Exception:
            recurrence_until = None

    end_time = start_time + timedelta(minutes=duration_minutes)

    return {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "participants": participants,
        "recurrence_type": recurrence_type,
        "recurrence_until": recurrence_until,
    }
