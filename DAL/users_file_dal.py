from importlib.util import set_loader
import json
import os
import sys

#Users Data layer that connects with json file which stores all the 
# users data except their login password which is stored in data base
class UsersFileDAL:
    def __init__(self):
        #The path of the json file
        self.__path = os.path.join(sys.path[0],'data/users.json')

    #Reading from json file and fetching all the users
    def read_file(self):
        with open(self.__path,'r') as f:
            data = json.load(f)
            return data

    #Writing updated data of users to json file
    def write_data_to_users_file(self, users_data):
        with open(self.__path,'w') as f:
            json.dump(users_data,f,indent=4)
            
        

    