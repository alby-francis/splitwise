
from flask import Flask
from core.services.api import init_api
from core.services.config import add_config
from core.services.db import db

def create_app():
    application = Flask(__name__)
    init_api(application)
    add_config(application)
    db.init_app(application)
    with application.app_context():
        return application