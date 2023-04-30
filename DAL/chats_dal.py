from pymongo import MongoClient
from bson import ObjectId



#Data layer of chats between 2 users
class ChatsDal:
    def __init__(self):

        #Connection established with Mongo DB
        self.__client = MongoClient(port=27017)

        #The data base in which the collection is located
        self.__db = self.__client["chatDB"]

        #The collection of chats with which this class connects
        self.__collection=self.__db["chats"]




    #Fetching chat data by id 
    def get_chat(self,chat_id):
        chat = self.__collection.find_one({ "_id" :chat_id })
        return chat

    #Adding new chat to db
    def add_chat(self,obj):
        self.__collection.insert_one(obj)
        return obj["_id"]   

    #Update existing chat
    def update_chat(self,id,obj):
        self.__collection.update_one({"_id" : id}, {"$set" : obj})
        return 'Updated!' 


