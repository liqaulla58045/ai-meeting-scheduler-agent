from .db import get_session, Meeting

def is_conflict(start_time, end_time, session=None):
    close_session = False
    if session is None:
        session = get_session()
        close_session = True

    conflicts = (
        session.query(Meeting)
        .filter(Meeting.start_time < end_time, Meeting.end_time > start_time)
        .all()
    )

    if close_session:
        session.close()

    return len(conflicts) > 0, conflicts

def create_meeting(title, participants, start_time, end_time, source="local"):
    session = get_session()
    conflict, _ = is_conflict(start_time, end_time, session=session)

    if conflict:
        session.close()
        return None, "Time slot conflicts with an existing meeting."

    meeting = Meeting(
        title=title,
        participants=participants,
        start_time=start_time,
        end_time=end_time,
        source=source
    )
    session.add(meeting)
    session.commit()
    session.refresh(meeting)
    session.close()
    return meeting, None

def get_all_meetings():
    session = get_session()
    meetings = session.query(Meeting).order_by(Meeting.start_time.asc()).all()
    session.close()
    return meetings
