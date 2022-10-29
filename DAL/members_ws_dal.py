from pymongo import MongoClient
from bson import ObjectId
import requests

#Data layer class that connects with a web service of members
#provided by another server
class MembersWSDal:
    def __init__(self):

        #URL of members web service
        self.__url = "http://localhost:5001/members"

    #Fetching all the members in the system
    def get_all_members(self):
        resp = requests.get(self.__url)
        return resp.json()

    #Adding new member to the system
    def add_member(self,obj):
        resp = requests.post(self.__url,json=obj)
        return resp.json() 

    #Updating an existing member ddetails
    def update_member(self,id,obj):
        resp = requests.put(self.__url+"/"+id,json=obj)
        return resp.json()

    #Delete a member by his id
    def delete_member(self,id):
        resp = requests.delete(self.__url+"/"+id)
        return resp.json()