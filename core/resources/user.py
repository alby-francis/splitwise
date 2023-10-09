import jwt

from core.models.user import  UserModel
from flask import jsonify, request, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from core.services.authentication import token_required
from flask_restful import Resource, reqparse

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)
    def post(self):
        data = UserLogin.parser.parse_args()
        email = data['email'].strip().lower()
        password = data['password'].strip()

        user = UserModel.find_by_email(email=email)
        if not user:
            return {'message' : 'No user found'},404

        if check_password_hash(generate_password_hash(user.password), password):
            token = jwt.encode({'id': user.id}, current_app.config['SECRET_KEY'], 'HS256')
            return {'token': token, 'response': user.json()}, 201

        return {'message': "Email/Password! doesn't match"}, 403


class UserSignup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True)
    parser.add_argument('name', required=False)
    parser.add_argument('password', required=False)
    parser.add_argument('mobile', required=False)

    def post(self):
        data = UserSignup.parser.parse_args()
        existing_data = UserModel.find_by_email(email=data['email'])
        if existing_data is not None:
            return jsonify({"message": "Email Already Exist"})

        new_user = UserModel(name=data['name'], email=data['email'], password=data['password'],
                             mobile_number=data['mobile'])
        try:
            new_user.save_to_db()
            new_user.create_login_token()
        except:
            return {"message": "Error saving user"}, 401
        return jsonify({"message": "New User is created!", "response": new_user.json()})


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True)
    parser.add_argument('name', required=False)
    parser.add_argument('password', required=False)
    parser.add_argument('mobile', required=False)


    @token_required

    def get(self,current_app):
        user = UserModel.find_by_email(id=current_app.id)
        if not user:
            return {"message": "User not found"},404

        return user.json(),201
    @token_required
    def patch(self,current_user):
        data = User.parser.parse_args()
        email = data.get('email', None)
        name = data.get('name', None)
        password = data.get('password', None)

        fetch_user = UserModel.find_by_id(id=current_user.id)
        existing_data = UserModel.find_by_email(email=email)

        if not fetch_user:
            return jsonify({"message": "User not found!"})

        if existing_data is not None:
            return jsonify({"message": "Email used by another user. Please update email"})

        fetch_user.email = email if email else fetch_user.email
        fetch_user.name = name if name else fetch_user.name
        fetch_user.password = password if password else fetch_user.password

        try:
            fetch_user.save_to_db()
        except Exception as e:
            return {'message': e}, 401

        return jsonify({"message": "Details Updated!"}), 201

    @token_required
    def delete(self,current_user):
        user = UserModel.find_by_email(id=current_user.id)
        if not user:
            return jsonify({"message": "User not found!"})
        try:
            user.save_to_db()
        except Exception as e:
            return {'message': e}

        return jsonify({"message": "Deleted!"}), 201


class AllUser(Resource):

    def get(self):
        users_items = UserModel.query.all()
        all_users = [user.json() for user in users_items]

        return jsonify(
            {"total": len(all_users),
             "users":
                 all_users
             }
        )