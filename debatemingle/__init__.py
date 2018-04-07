from flask import Flask
from debatemingle.zany.controllers import zany

app = Flask(__name__)

app.register_blueprint(zany, url_prefix='/')
