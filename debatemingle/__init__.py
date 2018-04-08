# app/__init__.py

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
CORS(app)
socketio = SocketIO(app, async_mode='eventlet')

# Load the views
from debatemingle import routes

# Load the config file
app.config.from_object('config')
