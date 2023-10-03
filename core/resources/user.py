from core.models.user import  UserModel
from flask import jsonify, request


# Read Specific
def get_one_user(id):
    user = UserModel.find_by_email(id=id)

    print(id)
    print(user)
    if not user:
        return jsonify({"message": "UserId not found"})

    user_data = {}
    user_data['id'] = user.id
    user_data['email'] = user.email
    user_data['name'] = user.name
    user_data['password'] = user.password

    return jsonify(user_data)


# Create User
def createUser():
    data = request.get_json()

    existing_data = UserModel.find_by_email(email=data['email'])
    if existing_data is not None:
        return jsonify({"message": "Email Already Exist"})

    new_user = UserModel(name=data['name'], email=data['email'], password=data['password'], mobile_number=data['mobile'])
    try:
        new_user.save_to_db()
        new_user.create_login_token()
    except:
        return {"message" : "Error saving user"}, 401
    return jsonify({"message": "New User is created!","response" : new_user.json()})


# Read All User
def all_users():
    users_items = UserModel.query.all()
    all_users = [user.json() for user in users_items]

    return jsonify(
        {"total": len(all_users),
         "users":
             all_users
         }
    )


# Edit/Update User Details
def edit_user(current_user):
    data = request.get_json()

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
        return {'message' : e},401

    return jsonify({"message": "Details Updated!"}),201


# Delete Specific
def remove_user(id):
    user = UserModel.find_by_email(id=id)

    if not user:
        return jsonify({"message": "User not found!"})

    try:
        user.save_to_db()
    except Exception as e:
        return {'message': e}

    return jsonify({"message": "Deleted!"}), 201


