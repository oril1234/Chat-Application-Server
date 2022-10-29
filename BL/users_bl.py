from DAL.users_db_dal import UsersDBDal
from DAL.users_file_dal import UsersFileDAL
from DAL.permissions_file_dal import PermissionsFileDAL


#Business logic class of users of the system
class UsersBL:
    def __init__(self):

        #Instance of users data layer connected to data base
        self.__users_db_dal = UsersDBDal()

        #Instance of users data layer connected to json file
        self.__users_file_dal = UsersFileDAL()
        
         #Instance of permissions data layer connected to json file
        self.__permissions_file_dal=PermissionsFileDAL()
        

    #Fetching all the users in the system by an orchestration 
    # of 3 data sources: 
    # 1. Users database collection
    # 2. The same users with their personal details like first and last 
    # name from json file
    # 3. Permissions of those users from json file 
    def get_users(self):
            
            users = []

            #All the users from data base
            users_from_db = self.__users_db_dal.get_all_users()

            #All the users from json file
            users_from_file = self.__users_file_dal.read_file()

            #All the users permissions from json file
            permissions_from_file = self.__permissions_file_dal.read_file()
        
            #Iterating all the users from json file
            for user in users_from_file:
                new_user={}

                #Adding the users details of the currently iterated user
                new_user["user_details"] = user


                #Match the the user from file with the same one from 
                # db by the id
                arr = list(filter(lambda x : 
                    str(x["_id"]) == user["id"],users_from_db))

                #Executed if user from db was found
                if len(arr) > 0:
                    new_user["authentication"]={}
                    new_user["authentication"]['username']=(
                        arr[0]['username'])

                    #Executed if user has already created an account
                    # and thus has a password
                    if 'password' in arr[0]:    
                        new_user["authentication"]['password']=(
                            arr[0]['password'])

                #Match the the user from file with his permissions 
                # in the permissions file by the id              
                arr = list(filter(lambda x : x["id"] == user["id"],
                permissions_from_file))

                #Executed if user's permissions were found
                if len(arr) > 0:
                    new_user["permissions"] = arr[0]["permissions"]
                
                users.append(new_user)

            return users


    #Get a specific user by his username if sent as arguments
    #  or by id if sent
    def get_user(self,username=None,id=None):

        user = {}

        #Executed if id was sent as an argument
        if id is not None:
            user["authentication"] = (
                self.__users_db_dal.get_user_by_id(id))
        
        #Executed if username was sent as an argument
        else:
            user["authentication"] = (
                self.__users_db_dal.get_user_by_username(username))
            id=str(user["authentication"]["_id"])
        
        user["authentication"].pop("_id",None)

        #Finding the user in users json file by the uder id from db
        users_from_file = self.__users_file_dal.read_file()
        arr = list(filter(lambda x : x["id"] ==
         id,users_from_file))
        if len(arr) > 0:
            user["user_details"] = arr[0]

        #Finding the user permissions in users permissions
        # json file by the uder id from db
        permissions_from_file = self.__permissions_file_dal.read_file()
        arr = list(filter(lambda x : x["id"] == id,
        permissions_from_file))
        if len(arr) > 0:
            user["permissions"] = arr[0]["permissions"]
            

        return user


    #creating a new user in the system by its admin
    def create_user(self,user):
        
        #Check if user doesn't already exist
        existed_user=self.__users_db_dal.get_user_by_username(
            user["authentication"]["username"])
        #Executed if a user with the same user name already exists
        if existed_user is not None:
            return None


        #Add useer to database with only username ( withput password
        # that will be added when the user will create an account)
        user_id=self.__users_db_dal.add_user(user["authentication"])

        #Add user personal details to json file
        self.__update_users_json(user_id,user)

        #Add user permission to json file
        self.__update_permissions_json(user_id,user)

        return user_id

    #Update an existing user
    def update_user(self,id,obj):

        #Update user in data base
        status=self.__users_db_dal.update_user(id,obj["authentication"])

        #Update user in json file
        self.__update_users_json(id,obj)

       #Update user permission in json file
        self.__update_permissions_json(id,obj)

        return status

    #Updating user details in json file
    def __update_users_json(self,db_user_id,user_info):
        
        #A user to add to users json
        user_for_json=user_info["user_details"]

        #Adding id from database to object of user
        #  that will be updated in json file
        user_for_json["id"]=db_user_id

        #Fetch current users from json
        current_users_data=self.__users_file_dal.read_file()

        #Wil be true if user with the same user id as the current user already
        #exists
        user_exists=False


        for index,user in enumerate(current_users_data):
            #Exwcuted if user with the same id from database was found
            if user["id"]==db_user_id:
                #Setting the updated details of the user if exists
                current_users_data[index]=user_for_json
                user_exists=True

        #Executed if current user is new and doesn't already exist        
        if not user_exists:
            current_users_data.append(user_for_json)

        #Json update    
        self.__users_file_dal.write_data_to_users_file(current_users_data)



    #Updatw users permissions in data base
    def __update_permissions_json(self,db_user_id,user_info):

        #Users permissions to add to users permissions file
        all_users_permissions=self.__permissions_file_dal.read_file()
        is_user_in_list=False
        for user_perm in all_users_permissions:

            #Update existing user permissions
            if user_perm["id"]==db_user_id:
                is_user_in_list=True
                user_perm["permissions"]=user_info["permissions"]
                break

        #Create user permission if they don't exist
        if not is_user_in_list:
            new_user_permissions={}
            new_user_permissions["id"]=db_user_id
            new_user_permissions["permissions"]=user_info["permissions"]
            all_users_permissions.append(new_user_permissions)


        #Write updated users permissions in file
        self.__permissions_file_dal.write_data_to_permissions_file(
            all_users_permissions
        )



    #Delete user by his id
    def delete_user(self,id):

        #Delete user from data base by id
        status = self.__users_db_dal.delete_user(id)

        #Fetch all users from json filr
        users_from_file = self.__users_file_dal.read_file()

        #Delete user from json file by id
        arr = list(filter(lambda x : x["id"] !=
         id,users_from_file))

        #Update all users in json file with the deleted one
        self.__users_file_dal.write_data_to_users_file(arr)

        #Fetch all user permissions from json filr
        permissions_from_file = self.__permissions_file_dal.read_file()
        
        #Delete user permission from file
        arr = list(filter(lambda x : x["id"] !=
         id,permissions_from_file))

        #Update all users permissions in json file withפוא the deleted one
        self.__permissions_file_dal.write_data_to_permissions_file(arr)
        return status