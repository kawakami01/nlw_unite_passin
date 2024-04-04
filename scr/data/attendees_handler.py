import uuid
from scr.models.repository.attendees_repository import AttendeesRepository
from scr.models.repository.events_repository import EventsRepository
from scr.http_types.http_request import HttpRequest
from scr.http_types.http_response import HttpResponse


class AttendeesHandler():
    def __init__(self) -> None:
        self.__attendees_repository = AttendeesRepository()
        self.__events_repository = EventsRepository()
        
    def registry(self, https_request: HttpRequest) -> HttpResponse:
        body = https_request.body
        event_id = https_request.param["event_id"]
        
        event_attendees_count = self.__events_repository.count_event_attendees(event_id)
        if (
            event_attendees_count["attendees_amount"]
            and event_attendees_count["maximum_attendees"] < event_attendees_count["attendees_amount"]
        ): raise Exception("The event is crowded!")
        
        body["uuid"] = str(uuid.uuid4())
        body["event_id"] = event_id
        self.__attendees_repository.insert_attendee(body)
        
        return HttpResponse(body=None, status_code=201)
        
    def find_attendee_badge(self, https_request: HttpRequest) -> HttpResponse:
        attendee_id = https_request.param["attendee_id"] # mudar isso se der erro
        badge = self.__attendees_repository.get_attendee_badge_by_id(attendee_id)
        if not badge: raise Exception("Attendee not found!")
        
        return HttpResponse(
            body={
                "badge": {
                    "name": badge.name,
                    "email": badge.name,
                    "event_title": badge.title
                }
            },
            status_code=200
        )
    
    def find_attendees_from_event(self, https_request: HttpRequest) -> HttpResponse:
        event_id = https_request.param["event_id"]
        attendees = self.__attendees_repository.get_attendees_by_event_id(event_id)
        if not attendees: raise Exception("Attendees not found")

        formatted_attendees = [
            {
                "id": attendee.id,
                "name": attendee.name,
                "email": attendee.email,
                "checked_in_at": attendee.checked_in_at,
                "created_at": attendee.created_at,
            }
            for attendee in attendees
        ]
        return HttpResponse(
            body={"attendees": formatted_attendees},
            status_code=200
        )
    