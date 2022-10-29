#Module of all endpoints related to users in the system
from flask import Blueprint,jsonify, make_response, request
from BL.users_bl import UsersBL

users = Blueprint('users', __name__)

#instance of users business logic
users_bl=UsersBL()

#Fetching all the users in the system 
@users.route("/", methods=['GET'])
def get_all_users():
    
    users = users_bl.get_users()
    return jsonify(users)
    



#Add new user to the system by the admin
@users.route("/", methods=['POST'])
def add_user():
    obj = request.json
    result = users_bl.create_user(obj)
    if result is None:
        return make_response({"error" : "User already exists!"},500)
    return jsonify(result)


#Update user details by the admin
@users.route("/<id>", methods=['PUT'])
def update_user(id):
    obj = request.json
    result = users_bl.update_user(id,obj)
    return jsonify(result)


#Delete user details by the admin
@users.route("/<id>", methods=['DELETE'])
def dlelete_user(id):
    result = users_bl.delete_user(id)
    return jsonify(result)