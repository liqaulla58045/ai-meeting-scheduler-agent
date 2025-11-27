from .db import get_session, Meeting


def is_conflict(start_time, end_time, session=None, ignore_meeting_id=None):
    """
    Check if the given time range conflicts with any existing meeting.
    Optionally ignore one meeting (for edits).
    """
    close_session = False
    if session is None:
        session = get_session()
        close_session = True

    query = session.query(Meeting).filter(
        Meeting.start_time < end_time,
        Meeting.end_time > start_time,
    )

    if ignore_meeting_id is not None:
        query = query.filter(Meeting.id != ignore_meeting_id)

    conflicts = query.all()

    if close_session:
        session.close()

    return len(conflicts) > 0, conflicts


def create_meeting(
    title,
    participants,
    start_time,
    end_time,
    source="local",
    recurrence_type="none",
    recurrence_until=None,
):
    """
    Create a new meeting if there is no time conflict.
    """
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
        source=source,
        recurrence_type=recurrence_type or "none",
        recurrence_until=recurrence_until,
    )
    session.add(meeting)
    session.commit()
    session.refresh(meeting)
    session.close()
    return meeting, None


def get_all_meetings():
    """
    Return all meetings ordered by start time.
    """
    session = get_session()
    meetings = session.query(Meeting).order_by(Meeting.start_time.asc()).all()
    session.close()
    return meetings


def edit_meeting(meeting_id, title=None, participants=None, start_time=None, end_time=None):
    """
    Edit an existing meeting. Only non-None fields are updated.
    Checks for time conflicts when changing time.
    """
    session = get_session()
    meeting = session.get(Meeting, meeting_id)

    if meeting is None:
        session.close()
        return False, f"Meeting with id {meeting_id} not found."

    new_start = start_time if start_time is not None else meeting.start_time
    new_end = end_time if end_time is not None else meeting.end_time

    conflict, _ = is_conflict(
        new_start,
        new_end,
        session=session,
        ignore_meeting_id=meeting_id,
    )

    if conflict:
        session.close()
        return False, "Updated time slot conflicts with another meeting."

    if title is not None:
        meeting.title = title
    if participants is not None:
        meeting.participants = participants

    meeting.start_time = new_start
    meeting.end_time = new_end

    session.commit()
    session.refresh(meeting)
    session.close()
    return True, None


def delete_meeting(meeting_id):
    """
    Delete an existing meeting by id.
    """
    session = get_session()
    meeting = session.get(Meeting, meeting_id)

    if meeting is None:
        session.close()
        return False, f"Meeting with id {meeting_id} not found."

    session.delete(meeting)
    session.commit()
    session.close()
    return True, None
