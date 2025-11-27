import os
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import pytz
from openai import OpenAI
import json

# Load API key from environment variable OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

IST = pytz.timezone("Asia/Kolkata")

def parse_meeting_request(user_input: str):
    """
    Uses OpenAI to extract:
    - title
    - date / time
    - duration (minutes)
    - participants (emails/names)
    """

    prompt = f"""
You are an assistant that extracts structured meeting details from user text.
Return ONLY a JSON object with the following keys:
- title (string)
- start (ISO datetime, no timezone, e.g. "2025-11-20 15:00")
- duration_minutes (integer)
- participants (comma-separated string of names or emails)

If any field is missing, make a reasonable assumption.

User request: "{user_input}"
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    # Get the model's text output
    raw_output = response.output[0].content[0].text

    try:
        data = json.loads(raw_output)
    except Exception:
        # Fallback simple parsing if JSON fails
        data = {
            "title": "Meeting",
            "start": (datetime.now(IST) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
            "duration_minutes": 30,
            "participants": ""
        }

    # Normalize
    start_dt = date_parser.parse(data.get("start"))
    if start_dt.tzinfo is None:
        start_dt = IST.localize(start_dt)

    duration = int(data.get("duration_minutes", 30))
    end_dt = start_dt + timedelta(minutes=duration)

    return {
        "title": data.get("title", "Meeting"),
        "start_time": start_dt,
        "end_time": end_dt,
        "participants": data.get("participants", "")
    }
