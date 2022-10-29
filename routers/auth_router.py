#This module consists of all the endpoints related to authentication
#of User to the system


from flask import Blueprint,jsonify, request, make_response
from BL.auth_bl import AuthBL
from BL.users_bl import UsersBL

auth = Blueprint('auth', __name__)

#Authentication business logic instance
auth_bl = AuthBL()

#Users business logic instance
users_bl=UsersBL()

#Login of user to the system
@auth.route("/login", methods=['POST'])
def login():

    #User credentials
    username = request.json["username"]
    password = request.json["password"]

    #Fetching the JWT related to the provided credentials
    token = auth_bl.get_token(username,password)

    #Reterning logged in user data if token found
    if token is not None:
        user_obj=users_bl.get_user(username=username)
        return make_response({"token" : token,"user":user_obj },200)
    
    #Executed if there's no token, meaning the user sent wrong
    #details
    return make_response({"error" : "You're not authorized" },401)


#Sign up of user to the system
@auth.route("/signup", methods=['POST'])
def signup():
    user=request.json
    response=auth_bl.create_user_account(user)

    #Executed if sign up succeeded
    if response["status"]==200:
        return make_response({"message" : response["message"]},200)

    #Executed if sign up failed, meaning there's already another user
    #account with identical user name
    return make_response({"error" :response["message"]
        },response["status"])


#End point for fetching data of logged in user
@auth.route("/logged_in_user", methods=['GET'])
def get_logged_in_user_data():

    #JWT used to identify the user
    token = request.headers.get('x-access-token')
    token_data=auth_bl.decode_token(token)

    #id of user from db
    id=token_data["userid"]

    #Get user data by his id
    user=users_bl.get_user(id=id)
    if user is not None:
        return make_response({"user":user },200)
    
    #Executed if no user details were found
    return make_response({"error" : "You're not authorized" },401)