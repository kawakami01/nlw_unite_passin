from typing import Dict
from scr.models.settings.connection import db_connection_handler
from scr.models.entities.events import Events
from scr.models.entities.attendees import Attendees
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from scr.errors.error_types.http_conflict import HttpConflictError


class EventsRepository:
    def insert_event(self, events_info: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                event = Events(
                    id=events_info.get("uuid"),
                    title=events_info.get("title"),
                    details=events_info.get("details"),
                    slug=events_info.get("slug"),
                    maximum_attendees=events_info.get("maximum_attendees"),
                )
                database.session.add(event)
                database.session.commit()

                return events_info
            except IntegrityError as e:
                raise HttpConflictError('Event already registered!') from e
            except Exception as exception:
                database.session.rollback()
                raise exception


    def get_event_by_id(self, event_id: str) -> Events:
        with db_connection_handler as database:
            try:
                return (
                    database.session.query(Events)
                    .filter(Events.id == event_id)
                    .one()
                )
            except NoResultFound:
                return None
            
    def count_event_attendees(self, event_id: str) -> Dict:
        with db_connection_handler as database:
            event_count = (
                database.session
                .query(Events)
                .join(Attendees, Events.id == Attendees.event_id)
                .filter(Events.id == event_id)
                .with_entities(
                    Events.maximum_attendees,
                    Attendees.id
                )
                .all()
            )
            if not len(event_count):
                return {
                    "maximun_attendees": 0,
                    "attendees_amount": 0
                }
            
            return {
                    "maximun_attendees": event_count[0].maximum_attendees,
                    "attendees_amount": len(event_count)
                }
