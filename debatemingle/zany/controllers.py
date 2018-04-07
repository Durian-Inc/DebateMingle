from flask import Blueprint


zany = Blueprint('main', __name__)


@zany.route('/')
def index():
    return "Zany"
