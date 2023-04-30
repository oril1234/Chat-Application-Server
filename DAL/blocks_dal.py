from pymongo import MongoClient
from bson import ObjectId



#Data layer of blocks collection, storing data of users blocking other 
# users, meaning they can't send messages to them via private chat
class BlocksDal:
    def __init__(self):

        #Connection established with Mongo DB
        self.__client = MongoClient(port=27017)

        #The data base in which the collection is located
        self.__db = self.__client["chatDB"]

        #The collection of blocks with which this class connects
        self.__collection=self.__db["blocks"]




    #Fetching the documents in which user 1 blocks user 2 and 
    #the other way around  
    def get_blocks(self,user1,user2):
        blocks = self.__collection.find({ 
        "$or":[
            {"_id.blocked_id":user1,"_id.blocker_id":user2},
            {"_id.blocked_id":user2,"_id.blocker_id":user1}
            ]
        })
        return blocks

    #Adding new document to blocks collection containing data regarding 
    #a user blocking another oner 
    def block_user(self,obj):
        self.__collection.insert_one({"_id" : obj})
        return "completed"  

    #Cancel blocking of a user by another user
    def unblock_user(self,obj):
        self.__collection.delete_one({"_id.blocked_id":obj["unblocked_id"],
             "_id.blocker_id":obj["unblocker_id"]})
        return 'Deleted!' 


