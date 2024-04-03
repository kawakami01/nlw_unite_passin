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
        