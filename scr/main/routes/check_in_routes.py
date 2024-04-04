from flask import Blueprint, jsonify, request
from scr.http_types.http_request import HttpRequest
from scr.data.check_in_handler import CheckInHandler
from scr.errors.error_handler import handle_error


check_in_route_bp = Blueprint("check_in_route", __name__)

@check_in_route_bp.route("/attendees/<attendee_id>/check-in", methods=["POST"])
def create_check_in(attendee_id):
    try:
        check_in_handler = CheckInHandler()
        http_request = HttpRequest(param={"attendee_id": attendee_id})
        http_response = check_in_handler.registry(http_request)
        
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code