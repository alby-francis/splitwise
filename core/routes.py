from core import app
from core.resources.transaction import createTransaction, total_shares
from core.services.authentication import token_required
from core.resources.user import get_one_user,createUser,all_users,edit_user,remove_user
from core.services.auth_view import login_view

# USERS ROUTE
@app.route("/")
def HOME():
    return {'message': 'System is working'}

#create User
@app.route("/signup", methods=['POST'])
def CREATE_USER():
    return createUser()

#Login method responsible for generating authentication tokens
@app.route('/login', methods=['POST'])
def LOGIN():
    return login_view()

#Read All User
@app.route('/user/all', methods=['GET'])
def GET_USERS():
    return all_users()

#Read Single User
@app.route('/user/<id>', methods=['GET'])
def GET_SINGLE_USER(id):
    return get_one_user(id)

#Edit User (Login token Required)
@app.route('/user', methods=['PUT'])
@token_required
def EDIT_SINGLE_USER(current_user):
    return edit_user(current_user)

#Delete Single User
@app.route('/user/<id>', methods=['DELETE'])
def REMOVE_SINGLE_USER(id):
    return remove_user(id)


@app.route('/transaction', methods=['POST'])
@token_required
def CREATE_TXN(current_user):
    return createTransaction(current_user)

@app.route('/balance', methods=['GET'])
@token_required
def TOTAL_SHARES(current_user):
    return total_shares(current_user)
