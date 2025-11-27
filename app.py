import streamlit as st
import pytz

from agent.db import init_db
from agent.nlp import parse_meeting_request
from agent.scheduler import create_meeting, get_all_meetings
from agent.calendar_integration import create_google_calendar_event

IST = pytz.timezone("Asia/Kolkata")


def init():
    init_db()


def main():
    st.set_page_config(
        page_title="AI Meeting Scheduler Agent",
        page_icon="📅",
        layout="wide",
    )

    st.title("📅 AI Meeting Scheduler Agent")
    st.write(
        "Enter natural language instructions to schedule meetings. "
        "The agent will parse your text, detect conflicts, and store meetings locally."
    )

    with st.sidebar:
        st.header("⚙️ Settings")
        use_google = st.checkbox(
            "Simulate Google Calendar integration", value=False
        )
        st.markdown("---")
        st.caption("Built for Rooman AI Internship Challenge")

    tab1, tab2 = st.tabs(["➕ Schedule Meeting", "📋 View Meetings"])

    # --- Tab 1: Schedule Meeting ---
    with tab1:
        st.subheader("Schedule via Natural Language")
        st.caption(
            "Example: *Schedule a 30-minute sync with Rahul tomorrow at 3 PM about project status*"
        )

        user_input = st.text_area("Your meeting request", height=120)

        if st.button("🔍 Understand & Propose Meeting"):
            if not user_input.strip():
                st.warning("Please enter a meeting request.")
            else:
                with st.spinner("Understanding your request..."):
                    parsed = parse_meeting_request(user_input)

                st.success("Proposed meeting details:")
                st.write(f"**Title:** {parsed['title']}")
                st.write(
                    f"**Participants:** {parsed['participants'] or 'Not specified'}"
                )
                st.write(
                    f"**Start:** {parsed['start_time'].strftime('%Y-%m-%d %H:%M')}"
                )
                st.write(
                    f"**End:** {parsed['end_time'].strftime('%Y-%m-%d %H:%M')}"
                )

                if st.button("✅ Confirm & Schedule"):
                    meeting, error = create_meeting(
                        title=parsed["title"],
                        participants=parsed["participants"],
                        start_time=parsed["start_time"],
                        end_time=parsed["end_time"],
                        source="google_calendar" if use_google else "local",
                    )

                    if error:
                        st.error(error)
                    else:
                        event_link = None
                        if use_google:
                            event = create_google_calendar_event(parsed)
                            event_link = event.get("event_link")

                        st.success("Meeting scheduled successfully!")
                        if event_link:
                            st.markdown(f"[Open calendar event]({event_link})")

    # --- Tab 2: View Meetings ---
    with tab2:
        st.subheader("All Scheduled Meetings")

        meetings = get_all_meetings()
        if not meetings:
            st.info("No meetings scheduled yet.")
        else:
            for m in meetings:
                with st.container():
                    st.markdown("---")
                    st.write(f"**Title:** {m.title}")
                    st.write(f"**Participants:** {m.participants or '-'}")
                    st.write(f"**Start:** {m.start_time.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**End:** {m.end_time.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Source:** {m.source}")
                    st.caption(
                        f"Created at: {m.created_at.strftime('%Y-%m-%d %H:%M')}"
                    )


if __name__ == "__main__":
    init()
    main()
