
from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from core.models.user import UserModel
from core import app
import jwt

def login_view():
    auth = request.get_json()
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic-realm= "Login required!"'})

    user = UserModel.find_by_email(email=auth['email'])
    if not user:
        return make_response('Could not verify user, Please signup!', 401, {'WWW-Authenticate': 'Basic-realm= "No user found!"'})

    if check_password_hash(generate_password_hash(user.password), auth.get('password')):
        #return jsonify(str(user.userId))
        token = jwt.encode({'id': user.id}, app.config['SECRET_KEY'], 'HS256')
        return make_response(jsonify({'token': token}), 201)

    return make_response('Could not verify password!', 403, {'WWW-Authenticate': 'Basic-realm= "Wrong Password!"'})

