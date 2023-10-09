from flask import request, make_response, jsonify
import jwt
from functools import wraps
from flask import current_app
from core.models.user import UserModel

# token decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # pass jwt-token in headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token: # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data)
            current_user = UserModel.find_by_id(id=data['id'])

        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)

        return f(current_user, *args, **kwargs)
    return decorator