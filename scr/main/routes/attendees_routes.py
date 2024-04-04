from flask import Blueprint, jsonify, request
from scr.data.attendees_handler import AttendeesHandler
from scr.http_types.http_request import HttpRequest


attendees_route_bp = Blueprint("attendees_route", __name__)

@attendees_route_bp.route("/events/<event_id>/register", methods=["POST"])
def create_attendees(event_id):
    attendees_handler = AttendeesHandler()
    http_request = HttpRequest(param={"event_id": event_id}, body=request.json)
    
    http_response = attendees_handler.registry(http_request)
    return jsonify(http_response.body), http_response.status_code

@attendees_route_bp.route("/attendees/<attendee_id>/badge", methods=["GET"])
def get_attendees_badge(attendee_id):
    attendees_handler = AttendeesHandler()
    http_request = HttpRequest(param={"attendee_id": attendee_id})
    
    http_response = attendees_handler.find_attendee_badge(http_request)
    return jsonify(http_response.body), http_response.status_code
