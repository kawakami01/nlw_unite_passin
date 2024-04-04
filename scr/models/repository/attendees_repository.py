from scr.models.settings.connection import db_connection_handler
from scr.models.entities.attendees import Attendees
from scr.models.entities import Events
from typing import Dict, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from scr.models.entities.check_ins import CheckIns
from scr.errors.error_types.http_conflict import HttpConflictError


class AttendeesRepository:
    def insert_attendee(self, attendee_info: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                attendee = (
                    Attendees(
                        id=attendee_info.get("uuid"),
                        name=attendee_info.get("name"),
                        email=attendee_info.get("email"),
                        event_id=attendee_info.get("event_id")
                    )
                )
                database.session.add(attendee)
                database.session.commit()

                return attendee_info
            except IntegrityError:
                raise HttpConflictError('Attendee already registered!')
            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_attendee_badge_by_id(self, attendee_id: str):
        with db_connection_handler as database:
            try:
                return (
                    database.session.query(Attendees)
                    .join(Events, Events.id == Attendees.event_id)
                    .filter(Attendees.id == attendee_id)
                    .with_entities(Attendees.name, Attendees.email, Events.title)
                    .one()
                )
            except NoResultFound:
                return None
            
    def get_attendees_by_event_id(self, event_id: str) -> List[Attendees]:
        with db_connection_handler as database:
            return (
                database.session
                .query(Attendees)
                .outerjoin(CheckIns, CheckIns.attendeeId==Attendees.id)
                .filter(Attendees.event_id==event_id)
                .with_entities(
                    Attendees.id,
                    Attendees.name,
                    Attendees.email,
                    CheckIns.created_at.label('checked_in_at'),
                    Attendees.created_at.label('created_at')
                )
                .all()
            )
