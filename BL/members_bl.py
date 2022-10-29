from DAL.members_ws_dal import MembersWSDal

#Business logic class of the members 
# (people who subscribe to mmovies) in the system
class MembersBL:
    def __init__(self):

        #Instance of the members data layer that connects
        # with a members web service provided by another server
        self.__members_ws_dal = MembersWSDal()
        
    #Fetching all the members 
    def get_all_members(self):
       members = self.__members_ws_dal.get_all_members()
       return members

    #Add new member to the system
    def add_member(self,obj):
        status = self.__members_ws_dal.add_member(obj)
        return status

    #Update an existing member in the system
    def update_member(self,id,obj):
         status = self.__members_ws_dal.update_member(id,obj)
         return status

    #Delete member by his id
    def delete_member(self,id):
        status = self.__members_ws_dal.delete_member(id)
        return status