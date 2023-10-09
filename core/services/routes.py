from core.resources.user import UserLogin, UserSignup

def init_routes(api):
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserSignup, '/signup')
    api.add_resource(User, '/user')
    api.add_resource(UserDelete, '/user/<int:id>')