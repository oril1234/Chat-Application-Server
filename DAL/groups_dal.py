from pymongo import MongoClient
from bson import ObjectId



#Data layer of groups of 2 users and more that chat with each other
class GroupsDal:
    def __init__(self):

        #Connection established with Mongo DB
        self.__client = MongoClient(port=27017)

        #The data base in which the collection is located
        self.__db = self.__client["chatDB"]

        #The collection of users with which this class connects
        self.__collection=self.__db["groups"]

    #Fetching group data by id 
    def get_group(self,group_id):
        user = self.__collection.find_one({ "_id" :group_id })
        return user
    
    #Fetching groups by given id's
    def get_groups_by_ids(self,groups_ids):
        groups = list(self.__collection.find({ "_id" :{"$in": groups_ids} }))
        return groups
    
    #Adding new user to db
    def add_group(self,obj):
        print(obj)
        self.__collection.insert_one(obj)
        return obj["_id"]   

    #Update exiating group
    def update_group(self,id,obj):
        self.__collection.update_one({"_id" : id}, {"$set" : obj})
        return 'Updated!' 

    #Delete group from db
    def delete_group(self,id):
        self.__collection.delete_one({"_id" :id})
        return 'Deleted!'  
