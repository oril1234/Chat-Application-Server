from pymongo import MongoClient
from bson import ObjectId



#Data layer of users that chats with one another within private chats 
#and groups
class UsersDal:
    def __init__(self):

        #Connection established with Mongo DB
        self.__client = MongoClient(port=27017)

        #The data base in which the collection is located
        self.__db = self.__client["chatDB"]

        #The collection of users with which this class connects
        self.__collection=self.__db["users"]

    #Fetching all the users
    def get_all_users(self):
        arr = []
        arr = list(self.__collection.find({}))
        return arr
    
    #Fetching all the users that are not in the provided list of users ids
    def get_all_users_except(self,users_ids):
        arr = []
        arr = list(self.__collection.find({ "_id" :{"$nin": users_ids} }))
        return arr


    #Fetching user's data by his email
    def get_user(self,email):
        user = self.__collection.find_one({ "_id" : email })
        return user

    #Fetching user by given ids
    def get_specified_users(self,users):
        users = list(self.__collection.find({ "_id" :{"$in": users} }))
        return users

    #Adding new user to db
    def add_user(self,obj):
        self.__collection.insert_one(obj)
        return obj["_id"]   

    #Update existing user's details in the db
    def update_user(self,id,obj):
        self.__collection.update_one({"_id" : ObjectId(id)}, {"$set" : obj})
        return 'Updated!' 

    #Delete user from db
    def delete_user(self,id):
        self.__collection.delete_one({"_id" : ObjectId(id)})
        return 'Deleted!'  
