import pytest

from .attendees_repository import AttendeesRepository
from scr.models.settings.connection import db_connection_handler

db_connection_handler.connect_to_database()

@pytest.mark.skip(reason="New registry on database")
def test_insert_attendee():
    event_id = "my-uuid"
    attendee_info = {
        "uuid": "my-uuid_attendee",
        "name": "attendee-name",
        "email": "email@email.com",
        "event_id": event_id
    }
    attendees_repository = AttendeesRepository()
    response = attendees_repository.insert_attendee(attendee_info)
    print(response)

@pytest.mark.skip(reason="...")
def test_get_attendee_badge_by_id():
    attendee_id = "uuid_attendee"
    attendee_repository = AttendeesRepository()
    attendee = attendee_repository.get_attendee_badge_by_id(attendee_id)

    print(attendee)
