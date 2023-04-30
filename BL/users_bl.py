from DAL.users_dal import UsersDal
from datetime import datetime, timedelta
import jwt
from flask_bcrypt import Bcrypt

#Business logic class of users of the system
class UsersBL:
    def __init__(self):

        #Object for hashing password
        self.bcrypt=Bcrypt()
        #Instance of users data layer connected to data base
        self.__users_dal = UsersDal()
        #Key by which JWT is created
        self.__key = "server_key"

        #The algorithm used to create the JWT
        self.__algorithm = "HS256"

        #Instance of the users data layer connected to data base
        self.__users_db_dal=UsersDal()


    #Get the JWT token according to the credentials
    def get_token(self,email, password):

        #user id from data base
        user_id = self.__check_correct_user_credentials(email,password)
        #Executed if no user was found
        if user_id is None:
            return user_id



        token =  jwt.encode({"userid" : user_id,
            "expiration":str(datetime.utcnow()+timedelta(minutes=200))
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


    #Verifying the JWT to check if it's valid
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
        user=self.__users_db_dal.get_user(user_id)
        return user
    

    #Checking there's a user with the provided email
    # and password, and if so returning his id
    def __check_correct_user_credentials(self,email, password):
        
        user=self.__users_db_dal.get_user(email)
        if (user is None or 
            not self.bcrypt.check_password_hash(user["password"],password)):
            return None
        
        return user["_id"]


    #Fetching all the users in the system 
    def get_users(self):

            #All the users from data base
            users = self.__users_dal.get_all_users()
            return users


    #Get a specific user by email
    def get_user(self,email):
        user=None
        user = self.__users_dal.get_user(email)
        return user


    #creating a new user in the system by its admin
    def create_user(self,user):
        
        #Check if user doesn't already exist
        existed_user=self.__users_dal.get_user(user["_id"])
        #Executed if a user with the same user name already exists
        if existed_user is not None:
            return None

        user["password"]=self.bcrypt.generate_password_hash(user["password"]).decode('utf-8')
        user_id=self.__users_dal.add_user(user)
        return user_id

    #Update an existing user
    def update_user(self,id,obj):

        #Update user in data base
        status=self.__users_dal.update_user(id,obj["authentication"])
        return status

    #Delete user by his id
    def delete_user(self,id):

        #Delete user from data base by id
        status = self.__users_dal.delete_user(id)

        return status