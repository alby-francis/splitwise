from core.resources.health import Health
from core.resources.transaction import Transaction, Balance
from core.resources.user import UserLogin, UserSignup, User


def init_routes(api):
    # user apis
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserSignup, '/signup')
    api.add_resource(User, '/user')
    api.add_resource(Health, '/')

    # transaction apis
    api.add_resource(Transaction, '/transaction')
    api.add_resource(Balance, '/balance')