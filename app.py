import streamlit as st
import pytz
import pandas as pd
from datetime import datetime
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.let_it_rain import rain
from streamlit_lottie import st_lottie 

from agent.db import init_db
from agent.nlp import parse_meeting_request
from agent.scheduler import create_meeting, get_all_meetings, edit_meeting, delete_meeting
from agent.calendar_integration import create_google_calendar_event
from calendar_view import show_calendar_view

# Lottie animation JSON (futuristic loading animation)
lottie_animation = {
    "url": "https://assets4.lottiefiles.com/packages/lf20_1pxqjqps.json"  # Futuristic loading
}

IST = pytz.timezone("Asia/Kolkata")

def init():
    init_db()

def main():
    st.set_page_config(
        page_title="AI Meeting Scheduler Agent", 
        page_icon="🚀", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for light mode only
    css = """
    <style>
    .main {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 50%, #e0e0e0 100%);
        color: #000000;
    }
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 50%, #e0e0e0 100%);
    }
    .stTitle {
        color: #007bff !important;
        text-shadow: 0 0 10px #007bff;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #007bff;
        box-shadow: 0 0 5px #007bff;
    }
    .stButton > button {
        background: linear-gradient(45deg, #007bff, #28a745);
        color: #ffffff;
        border: none;
        box-shadow: 0 0 10px #007bff;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px #007bff;
        transform: scale(1.05);
    }
    .meeting-card {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #007bff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.3);
        margin-bottom: 10px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ Settings")
        use_google = st.checkbox("Simulate Google Calendar integration", value=False)
        st.markdown("---")
        st.write("🚀 Futuristic AI Meeting Scheduler")
        st.caption("Enhanced for advanced features & animations")

    # Header with animation
    col1, col2 = st.columns([1, 3])
    with col1:
        st_lottie("https://assets4.lottiefiles.com/packages/lf20_1pxqjqps.json", height=100, key="lottie")
    with col2:
        st.title("🚀 Futuristic AI Meeting Scheduler")
        st.caption("Schedule meetings with natural language - now with recurring events & calendar view!")

    add_vertical_space(2)

    tab1, tab2, tab3 = st.tabs(["➕ Schedule Meeting", "📅 Calendar View", "📋 Manage Meetings"])

    with tab1:
        st.subheader("Schedule via Natural Language")
        st.caption("Example: *Schedule a 30-minute sync with Rahul tomorrow at 3 PM about project status every week*")

        user_input = st.text_area("Your request", height=120, key="input")

        if st.button("🔍 AI Analyze & Propose", type="primary"):
            if not user_input.strip():
                st.warning("Please enter a meeting request.")
            else:
                with st.spinner("AI analyzing your request..."):
                    parsed = parse_meeting_request(user_input)
                    st.session_state.parsed = parsed

                if 'parsed' in st.session_state:
                    parsed = st.session_state.parsed
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success("✅ Proposed Meeting Details")
                        st.write(f"**Title:** {parsed['title']}")
                        st.write(f"**Participants:** {parsed['participants'] or 'Not specified'}")
                        st.write(f"**Start:** {parsed['start_time'].strftime('%Y-%m-%d %H:%M IST')}")
                        st.write(f"**End:** {parsed['end_time'].strftime('%Y-%m-%d %H:%M IST')}")
                        if parsed.get('recurrence_type') != 'none':
                            st.write(f"**Recurrence:** {parsed['recurrence_type']} until {parsed['recurrence_until'].strftime('%Y-%m-%d') if parsed['recurrence_until'] else 'Ongoing'}")
                    with col2:
                        st.info("Preview")
                        # Simple preview card
                        with st.container():
                            st.markdown(f"""
                            <div class="meeting-card">
                                <h4>{parsed['title']}</h4>
                                <p><strong>With:</strong> {parsed['participants'] or 'Team'}</p>
                                <p><strong>When:</strong> {parsed['start_time'].strftime('%Y-%m-%d %H:%M')} - {parsed['end_time'].strftime('%H:%M')}</p>
                                {f'<p><strong>Repeats:</strong> {parsed.get("recurrence_type", "Once")}</p>' if parsed.get('recurrence_type') != 'none' else ''}
                            </div>
                            """, unsafe_allow_html=True)

        if 'parsed' in st.session_state and st.session_state.parsed:
            confirm = st.button("✅ Confirm & Schedule Meeting", type="primary")

            if confirm:
                parsed = st.session_state.parsed
                meeting, error = create_meeting(
                    title=parsed["title"],
                    participants=parsed["participants"],
                    start_time=parsed["start_time"],
                    end_time=parsed["end_time"],
                    source="google_calendar" if use_google else "local",
                    recurrence_type=parsed.get("recurrence_type", "none"),
                    recurrence_until=parsed.get("recurrence_until")
                )

                if error:
                    st.error(f"❌ Error: {error}")
                else:
                    st.success("🎉 Meeting scheduled successfully!")
                    if parsed.get('recurrence_type') != 'none':
                        st.balloons()
                        rain(emoji="🚀")
                    if use_google:
                        event = create_google_calendar_event(parsed)
                        st.info("📧 Simulated Google Calendar event created. In a real implementation, this would open your Google Calendar.")
                        # Avoid 404 by not linking to simulated URL
                        # st.markdown(f"[Open calendar event]({event.get('event_link', '')})")
                    st.session_state.parsed = None
                    st.rerun()

    with tab2:
        st.subheader("📅 Interactive Calendar View")
        show_calendar_view()

    with tab3:
        st.subheader("📋 Manage All Meetings")
        meetings = get_all_meetings()
        if not meetings:
            st.info("No meetings scheduled yet. Schedule one in the first tab!")
        else:
            # Export button
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("📤 Export to CSV"):
                    df = pd.DataFrame([
                        {
                            "ID": m.id,
                            "Title": m.title,
                            "Participants": m.participants or '',
                            "Start": m.start_time.strftime('%Y-%m-%d %H:%M'),
                            "End": m.end_time.strftime('%Y-%m-%d %H:%M'),
                            "Source": m.source,
                            "Recurrence": m.recurrence_type,
                            "Created": m.created_at.strftime('%Y-%m-%d %H:%M')
                        } for m in meetings
                    ])
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"meetings_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
                    # For PDF, simple text export for now
                    if st.button("📄 Export to PDF (Text)"):
                        pdf_text = "\n".join([f"{m.title} - {m.start_time} to {m.end_time}" for m in meetings])
                        st.download_button(
                            label="Download Text File",
                            data=pdf_text,
                            file_name="meetings.txt",
                            mime="text/plain"
                        )

            for m in meetings:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        with st.expander(f"**{m.title}** - {m.start_time.strftime('%Y-%m-%d %H:%M')} to {m.end_time.strftime('%H:%M')} ({m.recurrence_type if m.recurrence_type != 'none' else 'Once'})", expanded=False):
                            st.write(f"**Participants:** {m.participants or 'Not specified'}")
                            st.write(f"**Source:** {m.source}")
                            st.write(f"**Created:** {m.created_at.strftime('%Y-%m-%d %H:%M')}")
                            if m.recurrence_type != 'none':
                                st.write(f"**Recurrence:** {m.recurrence_type} until {m.recurrence_until.strftime('%Y-%m-%d') if m.recurrence_until else 'Ongoing'}")
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{m.id}"):
                            # Simple edit form
                            new_title = st.text_input("Title", value=m.title, key=f"title_{m.id}")
                            new_participants = st.text_input("Participants", value=m.participants or '', key=f"part_{m.id}")
                            success, err = edit_meeting(m.id, title=new_title, participants=new_participants)
                            if success:
                                st.success("Updated!")
                                st.rerun()
                            elif err:
                                st.error(err)
                    with col3:
                        if st.button("🗑️ Delete", key=f"del_{m.id}"):
                            success, err = delete_meeting(m.id)
                            if success:
                                st.success("Deleted!")
                                st.rerun()
                            elif err:
                                st.error(err)

if __name__ == "__main__":
    init()
    main()
