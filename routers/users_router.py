#Module of all endpoints related to users in the system
from flask import Blueprint,jsonify, make_response, request
from BL.users_bl import UsersBL

users = Blueprint('users', __name__)

#instance of users business logic
users_bl=UsersBL()


#Login of user to the system
@users.route("/login", methods=['POST'])
def login():

    #User credentials
    email = request.json["_id"]
    password = request.json["password"]

    #Fetching the JWT related to the provided credentials
    token = users_bl.get_token(email,password)
    #Reterning logged in user data if token found
    if token is not None:
        user_obj=users_bl.get_user(email)
        return make_response({"token" : token,"user":user_obj },200)
    
    #Executed if there's no token, meaning the user sent wrong
    #details
    return make_response({"error" : "You're not usersorized" },401)


#Sign up of user to the system
@users.route("/signup", methods=['POST'])
def signup():
    user=request.json
    response=users_bl.create_user(user)

    #Executed if sign up succeeded
    if response is not None:
        return make_response({"message" : "User successfully added"},200)

    #Executed if sign up failed, meaning there's already another user
    #account with identical user name
    return make_response({"error" :"User already exists"
        },500)


#End point for fetching data of logged in user
@users.route("/logged_in_user", methods=['GET'])
def get_logged_in_user_data():

    #JWT used to identify the user
    token = request.headers.get('x-access-token')
    token_data=users_bl.decode_token(token)

    #id of user from db
    id=token_data["userid"]

    #Get user data by his id
    user=users_bl.get_user(id)
    if user is not None:
        return make_response({"user":user },200)
    
    #Executed if no user details were found
    return make_response({"error" : "You're not authorized" },401)

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