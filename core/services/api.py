from flask_restful import Api

from core.services.routes import init_routes


def init_api(application):
    # Setup Flask Restful framework
    api = Api(application)
    init_routes(api)
    return False
