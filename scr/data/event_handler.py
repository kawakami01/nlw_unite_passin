from scr.models.repository.events_repository import EventsRepository
from scr.http_types.http_request import HttpRequest
from scr.http_types.http_response import HttpResponse
import uuid


class EventHandler:
    def __init__(self) -> None:
        self.__events_repository = EventsRepository()
        
    def register(self, https_request: HttpRequest) -> HttpResponse:
        body = https_request.body
        body["uuid"] = str(uuid.uuid4())
        self.__events_repository.insert_event(body)
        
        return HttpResponse(
            body={"eventId": body["uuid"]},
            status_code=200
        )
        
    def find_by_id(self,  https_request: HttpRequest) -> HttpResponse:
        event_id = https_request.param["event_id"]
        event = self.__events_repository.get_event_by_id(event_id)
        if not event: raise Exception("Event not found")
        
        event_attendees_count = self.__events_repository.count_event_attendees(event_id)

        return HttpResponse(
            body={
                "event": {
                    "id": event.id,
                    "title": event.title,
                    "details": event.details,
                    "slug": event.slug,
                    "maximum_attendees": event.maximum_attendees,
                    "attendees_amount": event_attendees_count["attendees_amount"]
                }
            },
            status_code=200
        )
