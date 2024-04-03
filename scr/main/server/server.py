from flask import Flask
from flask_cors import CORS
from scr.models.settings.connection import db_connection_handler

db_connection_handler.connect_to_database()

app = Flask(__name__)
CORS(app)

from scr.main.routes.event_routes import event_route_bp
app.register_blueprint(event_route_bp)
