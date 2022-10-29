from pymongo import MongoClient
from bson import ObjectId

#Data layer of users that connects with users collection
#in Mongo Data bas
class UsersDBDal:
    def __init__(self):

        #Connection established with Mongo DB
        self.__client = MongoClient(port=27017)

        #The data base in which the collection is located
        self.__db = self.__client["usersDB"]

        #The collection of users with which this class connects
        self.__collection=self.__db["users"]

    #Fetching all the users
    def get_all_users(self):
        arr = []
        arr = list(self.__collection.find({}))
        return arr

    #Fetching user's data by his id
    def get_user_by_id(self,id):
        user = self.__collection.find_one({ "_id" : ObjectId(id) })
        return user

    #Fetching user's data by his username
    def get_user_by_username(self,username):
        user = self.__collection.find_one({ "username" : username })
        return user

    #Adding new user to db
    def add_user(self,obj):
        self.__collection.insert_one(obj)
        return str(obj["_id"])    

    #Update existing user's details in the db
    def update_user(self,id,obj):
        self.__collection.update_one({"_id" : ObjectId(id)}, {"$set" : obj})
        return 'Updated!' 

    #Delete user from db
    def delete_user(self,id):
        self.__collection.delete_one({"_id" : ObjectId(id)})
        return 'Deleted!'  
