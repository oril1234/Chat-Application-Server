from pymongo import MongoClient
from bson import ObjectId



#Data layer of details of memberships of users in groups
class GroupsMembersDal:
    def __init__(self):

        #Connection established with Mongo DB
        self.__client = MongoClient(port=27017)

        #The data base in which the collection is located
        self.__db = self.__client["chatDB"]

        #The collection of groups users belong to
        self.__collection=self.__db["groups_members"]

    #Fetching details of membership of user in a group
    def get_group_membership(self,member_id,group_id):
        group_member_record = self.__collection.find_one({"_id.groupID":group_id,
        "_id.userID": member_id})
        return group_member_record  
    
    #Fetching all user memberships in groups
    def get_user_groups_membership(self,email):
        arr = []
        arr = list(self.__collection.find({"_id.userID":email}))
        return arr

    #Get the data of all the memberships of members in a given group, 
    #even those that already existed or were removed by the group admin, 
    # as long as those memberships haven't been deleted completely.
    def get_all_undeleted_memberships(self,group_id):
        arr = []
        arr = list(self.__collection.find({"_id.groupID":group_id}))
        return arr
    
    #Fetching data of all the active memberships in a given group, 
    #meaning they were not removed by group adminm or exited the group
    #themselves
    def get_group_memberships(self,group_id):
        arr = []
        arr = list(self.__collection.find({"_id.groupID":group_id,
                        "remove_date":{"$exists":False},
                         "exit_date":{"$exists":False} }))
        return arr
    

    #Adding a batch of new members to groups
    def add_members_to_group(self,obj):
        print(obj)
        status=self.__collection.insert_many(obj)
        return status.inserted_ids  

    #Update existing group member details
    def update_group_member(self,member_id,group_id,obj):
        self.__collection.update_one({"_id.groupID":group_id,
        "_id.userID": member_id}, {"$set" : obj})
        return 'Updated!' 

    #Delete membership of a group member
    def delete_member_from_group(self,group_id,user_id):
        self.__collection.delete_one({"_id" :{"userID" :user_id,
                                              "groupID":group_id }})
        return 'Deleted!'  
