

from datetime import datetime, timedelta
from pickle import NONE

from DAL.users_db_dal import UsersDBDal
from DAL.users_file_dal import UsersFileDAL
from DAL.permissions_file_dal import PermissionsFileDAL
import jwt

#Business logic class of authentication of users
class AuthBL:
    def __init__(self):

        #Key by which JWT is created
        self.__key = "server_key"

        #The algorithm used to create the JWT
        self.__algorithm = "HS256"

        #Instance of the users data layer connected to data base
        self.__users_db_dal=UsersDBDal()

        #Instance of the users data layer connected to json file of users
        #details
        self.__users_file_dal=UsersFileDAL()


    #Get the JWT token according to the credentials
    def get_token(self,username, password):

        #user id from data base
        user_id = self.__check_correct_user_credentials(username,password)

        #Executed if no user was found
        if user_id is None:
            return user_id

        #Fetching all the users from json and filtering them 
        #according to user id
        users_from_file=self.__users_file_dal.read_file()
        filtered_users_by_user_id=list(filter(lambda 
            user:user["id"]==user_id,
        users_from_file))

        token = None

        #Executed if user was found in file
        if len(filtered_users_by_user_id)>0:

            #The duration of time the user is alloeded to stay logged in
            session_timeout=filtered_users_by_user_id[0]["sessionTimeout"]

            #Encoding the JWT with the data of user id and
            #the expiration time of JWT using key and algorithm
            token = jwt.encode({"userid" : user_id,
            "expiration":str(datetime.utcnow()+timedelta(minutes=session_timeout))
            }, self.__key, self.__algorithm)

        return token
    
    #Decoding token in order to get user id from it
    def decode_token(self, token):
        data=None
        try:
            data = jwt.decode(token, self.__key, self.__algorithm)
        except:
            return None
        return data


    #Verifying the JWT to check it's valid
    def verify_token(self, token):
        data=self.decode_token(token)
        

        current_time=datetime.utcnow()
        expiration=datetime.strptime(data["expiration"],
         '%Y-%m-%d %H:%M:%S.%f')

        #Executed if token expired
        if current_time>expiration:
            return None

        user_id = data["userid"]

        #Fetching user credentials by the his id fetched from decoded JWT
        user=self.__users_db_dal.get_user_by_id(user_id)
        return user
    

    #Checking there's a user with the provided username 
    # and password, and if so returning his id
    def __check_correct_user_credentials(self,username, password):
        user=self.__users_db_dal.get_user_by_username(username)
        if (user is None or "password" not in user 
            or user["password"]!=password):
            return None
        
        return str(user["_id"])

    #Creating a user account after he was previously added to
    #  the system by the system admin
    def create_user_account(self,obj):
        user=self.__users_db_dal.get_user_by_username(obj["username"])
        if user is None:
            return {"message":"You are not authorized to register account"+
            " under this username.","status":401}
        if "password" in user:
            return {"message":"An account under the user name "+user["username"]
             +" already exists.","status":500}            
        response=self.__users_db_dal.update_user(user["_id"],obj)

        return {"message":response,"status":200}




