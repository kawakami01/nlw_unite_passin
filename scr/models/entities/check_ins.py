from scr.models.settings.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func


class CheckIns(Base):
    __tablename__ = "check_ins"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    attendeeId = Column(String, ForeignKey("attendees_id"))

    def __repr__(self):
        return f"CheckIns [attendee_id={self.attendeeId}"
