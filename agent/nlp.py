from datetime import datetime, timedelta
from dateutil import parser as date_parser
import pytz
import re

IST = pytz.timezone("Asia/Kolkata")

def parse_meeting_request(user_input: str):
    """
    Offline/local parser for meeting extraction without external APIs.

    Extracts best-effort:
    - title (after word 'about', else 'Meeting')
    - start_time (understands 'today', 'tomorrow', times like '4 pm', '11:30 am')
    - duration_minutes (e.g. '30 minutes', '1 hour')
    - participants (after word 'with')
    """

    text = user_input.strip()
    lower = text.lower()

    # Defaults
    now = datetime.now(IST)
    start_time = now + timedelta(hours=1)
    duration_minutes = 30
    title = "Meeting"
    participants = ""

    # Duration: "30 minutes", "1 hour", "2 hrs"
    dur = re.search(r"(\d+)\s*(minute|min|hour|hr|hours|hrs)", lower)
    if dur:
        num = int(dur.group(1))
        unit = dur.group(2)
        if "hour" in unit or "hr" in unit:
            duration_minutes = num * 60
        else:
            duration_minutes = num

    # Date keywords
    if "tomorrow" in lower:
        base_date = now + timedelta(days=1)
    else:
        base_date = now

    if "today" in lower:
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
            microsecond=0
        )
    else:
        # If no explicit time, set to next full hour
        start_time = base_date.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    # Participants: after word "with"
    with_idx = lower.find("with")
    if with_idx != -1:
        participants = text[with_idx + len("with"):].strip()
        # Stop at "about" if present after "with"
        about_idx = participants.lower().find("about")
        if about_idx != -1:
            participants = participants[:about_idx].strip()

    # Title/topic: after word "about"
    about_idx_full = lower.find("about")
    if about_idx_full != -1:
        title = text[about_idx_full + len("about"):].strip().capitalize() or "Meeting"
    else:
        # Fallback: small cleaned version of original text as title
        title = text[:60] + ("..." if len(text) > 60 else "")

    # Recurrence
    recurrence_type = "none"
    recurrence_until = None
    if "every day" in lower:
        recurrence_type = "daily"
        recurrence_until = start_time + timedelta(days=365)  # default 1 year
    elif "every week" in lower:
        recurrence_type = "weekly"
        recurrence_until = start_time + timedelta(weeks=52)
    elif "every month" in lower:
        recurrence_type = "monthly"
        recurrence_until = start_time + timedelta(days=365)

    end_time = start_time + timedelta(minutes=duration_minutes)

    return {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "participants": participants,
        "recurrence_type": recurrence_type,
        "recurrence_until": recurrence_until
    }
