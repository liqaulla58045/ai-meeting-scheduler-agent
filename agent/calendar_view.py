import streamlit as st
import pandas as pd
from agent.scheduler import get_all_meetings


def show_calendar_view():
    """
    Simple calendar-like view of meetings grouped by date.
    """
    meetings = get_all_meetings()
    if not meetings:
        st.info("No meetings scheduled yet.")
        return

    rows = []
    for m in meetings:
        rows.append({
            "Date": m.start_time.date(),
            "Title": m.title,
            "Time": f"{m.start_time.strftime('%H:%M')} - {m.end_time.strftime('%H:%M')}",
            "Participants": m.participants or "",
            "Recurrence": (
                m.recurrence_type if getattr(m, "recurrence_type", "none") != "none"
                else "Once"
            ),
        })

    df = pd.DataFrame(rows).sort_values(["Date", "Time"])

    st.write("### 📅 Calendar View (by Date)")

    unique_dates = sorted(df["Date"].unique())
    if not unique_dates:
        st.info("No meetings to show.")
        return

    selected_date = st.date_input(
        "Select date to view",
        value=unique_dates[0],
        min_value=unique_dates[0],
        max_value=unique_dates[-1],
    )

    day_df = df[df["Date"] == selected_date]
    if day_df.empty:
        st.info("No meetings on this date.")
    else:
        st.dataframe(day_df.reset_index(drop=True), use_container_width=True)
