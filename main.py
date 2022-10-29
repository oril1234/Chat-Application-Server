#Main module that listens to API calls and
#routes them to the corresponding routes

from asyncio import threads
from flask import Flask,request, make_response
import json
from bson import ObjectId
from flask_cors import CORS
from routers.auth_router import auth
from routers.users_router import users
from routers.movies_router import movies
from routers.members_router import members
from routers.subscriptions_router import subscriptions
from BL.auth_bl import AuthBL

#Serializer class used to format data that 
#consists of data type of ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj) :
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self,obj)

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


app.json_provider_class = JSONEncoder

#Executed before routing any request in order to ensure
#the user who sent the request is authorised by checking if
#he sent a valid json web token
@app.before_request
def check_token():

    #Instance of authentication business logic class
    auth_bl=AuthBL()
    
    #Executed only if the sent request is not of type options and the 
    # rquest is not related to authentication (login or sign up of user)
    if request.method!="OPTIONS" and "/auth" not in request.url:
        #Executed if the user added to request headers the JWT
        if request.headers and request.headers.get('x-access-token'):

            #The JWT
            token = request.headers.get('x-access-token')
            
            #Checking the JWT is valid and if not sending error response 
            exist = auth_bl.verify_token(token)
            if exist is None:
                return make_response({"error" : "Not authorized"},401)
        
        #Executed if user did not send JWT
        else:
            return make_response({"error" : "No token provided"},401)

#Registering all API calls related to authentication
app.register_blueprint(auth, url_prefix="/auth")

#Registering all API calls related to the system's users
app.register_blueprint(users, url_prefix="/users")

#Registering all API calls related to movies in the system
app.register_blueprint(movies, url_prefix="/movies")

#Registering all API calls related to members who can subscribe to movies
app.register_blueprint(members, url_prefix="/members")

#Registering all API calls related to subscriptions of movies by members
app.register_blueprint(subscriptions, url_prefix="/subscriptions")

app.run(host="0.0.0.0")
