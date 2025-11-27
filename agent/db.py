import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    participants = Column(String, nullable=True)  # comma-separated emails/names
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    source = Column(String, default="local")  # local / google_calendar
    created_at = Column(DateTime, default=datetime.utcnow)

DB_PATH = os.path.join("data", "meetings.db")
os.makedirs("data", exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return SessionLocal()
