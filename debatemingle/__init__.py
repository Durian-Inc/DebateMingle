# app/__init__.py

from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from debatemingle import routes

# Load the config file
app.config.from_object('config')
