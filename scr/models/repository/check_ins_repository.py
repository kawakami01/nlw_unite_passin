from scr.models.settings.connection import db_connection_handler
from scr.models.entities.check_ins import CheckIns
from sqlalchemy.exc import IntegrityError
from scr.errors.error_types.http_conflict import HttpConflictError

db_connection_handler.connect_to_database()


class CheckInRepository:
    def insert_check_in(self, attendee_id: str) -> str:
        with db_connection_handler as database:
            try:
                check_in = (
                    CheckIns(attendeeId=attendee_id)
                )
                database.session.add(check_in)
                database.session.commit()

                return attendee_id
            except IntegrityError as e:
                raise HttpConflictError('Check-in already registered!') from e
            except Exception as exception:
                database.session.rollback()
                raise exception
