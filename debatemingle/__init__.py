# app/__init__.py

from flask import Flask
from flask_socketio import SocketIO

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
socketio = SocketIO(app, async_mode='eventlet')

# Load the views
from debatemingle import routes

# Load the config file
app.config.from_object('config')
