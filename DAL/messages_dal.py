from pymongo import MongoClient
from bson import ObjectId



#Data layer of messages being sent between users in chat and groups
class MessagesDal:
    def __init__(self):

        #Connection established with Mongo DB
        self.__client = MongoClient(port=27017)

        #The data base in which the collection is located
        self.__db = self.__client["chatDB"]

        #The collection of messages with which this class connects
        self.__collection=self.__db["messages"]



    #Fetching all the messages of a given chat between 2 users
    def get_chat_messages(self,chatID):
        user = self.__collection.find({ "chatID" : chatID })
        return user
    
    #Fetching all the messages of a given group between nultiple users
    def get_group_messages(self,groupID):
        user = self.__collection.find({ "groupID" :groupID})
        return user

    #Adding new message to collection
    def add_message(self,obj):
        self.__collection.insert_one(obj)
        return obj["_id"]   
