import streamlit as st
from streamlit_calendar import calendar
from agent.scheduler import get_all_meetings
from datetime import datetime

def show_calendar_view():
    st.subheader("📅 Calendar View")

    meetings = get_all_meetings()

    events = []
    for m in meetings:
        events.append({
            "title": m.title,
            "start": m.start_time.isoformat(),
            "end": m.end_time.isoformat(),
            "backgroundColor": "#FF6B6B" if m.source == "google_calendar" else "#4ECDC4",
            "borderColor": "#FF6B6B" if m.source == "google_calendar" else "#4ECDC4",
        })

    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "22:00:00",
        "initialView": "dayGridMonth",
        "editable": False,
        "selectable": True,
        "events": events,
    }

    calendar(calendar_options)
