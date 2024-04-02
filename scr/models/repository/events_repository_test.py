import pytest
from .events_repository import EventsRepository
from scr.models.settings.connection import db_connection_handler

db_connection_handler.connect_to_database()


@pytest.mark.skip(reason="New registry on database")
def test_insert_event():
    event = {
        "uuid": "my-uuid",
        "title": "my-title",
        "slug": "my-slug",
        "maximum_attendees": 20,
    }

    event_repository = EventsRepository()
    response = event_repository.insert_event(event)
    print(response)


@pytest.mark.skip(reason="Not necessary")
def test_get_event_by_id():
    event_id = "my-uuid"
    events_repository = EventsRepository()
    response = events_repository.get_event_by_id(event_id)
    print(response)
