from pymongo import MongoClient
from bson import ObjectId



#Data layer of details of users in chats, including their idsm chats ids, 
#number of unread messages in each chat, and the users they chat with
class UsersChatsDal:
    def __init__(self):

        #Connection established with Mongo DB
        self.__client = MongoClient(port=27017)

        #The data base in which the collection is located
        self.__db = self.__client["chatDB"]

        #The collection of chats users belong to
        self.__collection=self.__db["users_chats"]
        
    #Fetching data of a given user in all chats
    def get_user_chats_by_user(self,email):
        arr = []
        arr = list(self.__collection.find({"_id.userID":email}))
        return arr

    #Fetching the document of a given user and chat id
    def get_chat_user(self,user_id,chat_id):
        chat_record = self.__collection.find_one({"_id.chatID":chat_id,
        "_id.userID": user_id})
        return chat_record

    #Fetching details of all the partner of a given user in different chats
    def get_partners_chats_details(self,chats_ids,user_id):
        chats_record = self.__collection.find({"_id.chatID":{"$in":chats_ids},
        "_id.userID": { "$ne": user_id }})
        return chats_record

    #Add new details of a user in a chat
    def add_user_to_chat(self,obj):
        self.__collection.insert_one(obj)
        return "Inserted"   

    #Update existing chat user's details in the collection
    def update_chat_user(self,user_id,chat_id,obj):
        self.__collection.update_one({"_id.chatID":chat_id,
        "_id.userID": user_id},{"$set" : obj})
        return 'Updated!' 

    #Delete details of user in a chat
    def delete_user_from_chat(self,user_id,chat_id):
        self.__collection.delete_one({"_id.userID":user_id,
                                              "_id.chatID":chat_id})
        return 'Deleted!'  
