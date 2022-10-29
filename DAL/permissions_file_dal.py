import json
import os
import sys

#Permissions data layer that connects with permissions json file
class PermissionsFileDAL:
    def __init__(self):
        #Path of json file
        self.__path = os.path.join(sys.path[0],'data/permissions.json')

    #Reading and fetching all the permissions data in the json file
    def read_file(self):
        with open(self.__path,'r') as f:
            data = json.load(f)
            return data

    #Writing updated data to the json file
    def write_data_to_permissions_file(self, permissions):
         with open(self.__path,'w') as f:
            json.dump(permissions,f,indent=4)
            
        

    