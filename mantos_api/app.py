from flask import Flask

from mantos_api.extensions import cors
from mantos_api.extensions import database


def create_app():
    app = Flask(__name__)

    database.init_app(app)
    cors.init_app(app)

    return app
