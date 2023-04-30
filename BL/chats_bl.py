from DAL.users_chats_dal import UsersChatsDal
from datetime import datetime, timedelta
import jwt
from flask_bcrypt import Bcrypt

#Business logic class of chats between two users
class ChatsBL:
    def __init__(self):

        #Object for hashing password
        self.bcrypt=Bcrypt()


        #Instance of users chats data layer connected to data base
        self.__users_chats_dal=UsersChatsDal()  

    #Delete user from chat, meaining the chat will still exist but 
    #the user won't see it 
    def delete_user_from_chat(self,chat_id,user_id):
        status=self.__users_chats_dal.delete_user_from_chat(
            user_id,chat_id)
        return status
    
