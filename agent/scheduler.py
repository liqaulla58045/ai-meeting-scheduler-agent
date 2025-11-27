from agent.db import get_session, Meeting
from datetime import datetime, timedelta
from typing import Optional, Tuple

def check_conflict(start_time: datetime, end_time: datetime) -> bool:
    session = get_session()
    try:
        conflicts = session.query(Meeting).filter(
            Meeting.start_time < end_time,
            Meeting.end_time > start_time
        ).all()
        return len(conflicts) > 0
    finally:
        session.close()

def create_meeting(title: str, participants: Optional[str], start_time: datetime, end_time: datetime, source: str = "local", recurrence_type: str = "none", recurrence_until: Optional[datetime] = None) -> Tuple[Optional[Meeting], Optional[str]]:
    if recurrence_type == "none":
        if check_conflict(start_time, end_time):
            return None, "Conflict detected with existing meeting."
        meeting = Meeting(
            title=title,
            participants=participants,
            start_time=start_time,
            end_time=end_time,
            source=source,
            recurrence_type=recurrence_type,
            recurrence_until=recurrence_until
        )
        session = get_session()
        try:
            session.add(meeting)
            session.commit()
            return meeting, None
        except Exception as e:
            session.rollback()
            return None, str(e)
        finally:
            session.close()
    else:
        # Handle recurring meetings
        meetings = []
        current_start = start_time
        current_end = end_time
        while current_start <= recurrence_until:
            if check_conflict(current_start, current_end):
                return None, f"Conflict detected for recurring instance on {current_start.strftime('%Y-%m-%d %H:%M')}."
            meetings.append(Meeting(
                title=title,
                participants=participants,
                start_time=current_start,
                end_time=current_end,
                source=source,
                recurrence_type=recurrence_type,
                recurrence_until=recurrence_until
            ))
            if recurrence_type == "daily":
                current_start += timedelta(days=1)
                current_end += timedelta(days=1)
            elif recurrence_type == "weekly":
                current_start += timedelta(weeks=1)
                current_end += timedelta(weeks=1)
            elif recurrence_type == "monthly":
                # Approximate monthly as 30 days
                current_start += timedelta(days=30)
                current_end += timedelta(days=30)
            else:
                break
        session = get_session()
        try:
            for m in meetings:
                session.add(m)
            session.commit()
            return meetings[0], None  # Return first meeting as representative
        except Exception as e:
            session.rollback()
            return None, str(e)
        finally:
            session.close()

def get_all_meetings():
    session = get_session()
    try:
        return session.query(Meeting).order_by(Meeting.start_time).all()
    finally:
        session.close()

def edit_meeting(meeting_id: int, **updates) -> Tuple[bool, Optional[str]]:
    session = get_session()
    try:
        meeting = session.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            return False, "Meeting not found."
        for key, value in updates.items():
            if hasattr(meeting, key):
                setattr(meeting, key, value)
        session.commit()
        return True, None
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()

def delete_meeting(meeting_id: int) -> Tuple[bool, Optional[str]]:
    session = get_session()
    try:
        meeting = session.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            return False, "Meeting not found."
        session.delete(meeting)
        session.commit()
        return True, None
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()
