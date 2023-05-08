from DAL.groups_dal import GroupsDal
from DAL.groups_members_dal import GroupsMembersDal
from datetime import datetime
from dateutil import parser

#Business logic class of groups
class GroupsBL:
    def __init__(self):

        #Instance of groups data layer connected to data base
        self.__groups_dal=GroupsDal()

        #Instance of groups members data layer connected to data base
        self.__groups_members_dal=GroupsMembersDal()    


    #Adding new group to db
    def create_group(self,group):
        status=self.__groups_dal.add_group({"_id":group["group_id"],
                                            "name":group["group_name"],
        "creator":group["creator"],"last_activity":group["last_activity"]})
        if status is None:
            return None
        
        #Add members to the newly created group
        result=self.add_new_group_members(group["group_id"],group["members"])
        return result

    #Get shared groups of 2 users
    def get_shared_groups_by_user_ids(self,user_id1,user_id2):

        #IDs of all the the groups user 1 is in
        user1_active_groups_ids=self.get_user_groups_memberships(
            user_id1)[1]
        #IDs of all the the groups user 2 is in
        user2_active_groups_ids=self.get_user_groups_memberships(
            user_id2)[1]
        
        #Storing the groups both user 1 and user 2 are in
        shared_groups=self.get_shared_groups_by_groups_ids(
            user1_active_groups_ids,user2_active_groups_ids)
        shared_groups=list(filter(lambda group:"close_date" not in group,shared_groups))
        return shared_groups
 
    #Fetching all the mutual groups of given groups
    def get_shared_groups_by_groups_ids(self,groups_ids1,groups_ids2):
        shared_groups_ids=list(set(groups_ids1).intersection(
            groups_ids2))
        shared_groups=self.__groups_dal.get_groups_by_ids(shared_groups_ids)       
        return shared_groups

    #Fetching details of all user memberships in groups, including
    #groups the user is no longer a member in, but he still did not
    #completely delete the details of his past memberships in them
    def get_user_groups_memberships(self,user_id):

        #All user present and past undeleted memberships
        all_user_groups_memberships=(
        self.__groups_members_dal.get_user_groups_membership(
        user_id
        ))

        #Details of only the active groups memberships of current user
        user_active_groups_memberships=list(filter(
            lambda group_membership:("exit_date" not in group_membership) 
            and ("remove_date" not in group_membership),
            all_user_groups_memberships))
        user_active_groups_ids=list(map(lambda group_membership:
                            group_membership["_id"]["groupID"],
                            user_active_groups_memberships))
        return (all_user_groups_memberships,user_active_groups_ids)
    
    #Adding new members to group
    def add_new_group_members(self,group_id,new_members):
        
        users_in_group_list=[]
        result=None

        #Iterating all the new group members to add them to group 
        for member in new_members:

            #Check if current member is not already a member 
            #of the group
            group_membership=(
                self.__groups_members_dal.get_group_membership(
                member["_id"],group_id))
            
            #Executed if member is already in the group
            if group_membership is not None:
                if ("remove_date" in group_membership
                    or "exit_date" in group_membership):
                    self.__groups_members_dal.delete_member_from_group(
                        group_id,member["_id"]
                    )

            #Add a new membership of current member to group
            users_in_group_list.append({"_id":{"userID":member["_id"],
            "groupID":group_id},"unread_messages_number":0,
            "join_date":datetime.fromisoformat(
                datetime.now().isoformat())})
        result=self.__groups_members_dal.add_members_to_group(users_in_group_list)

        return result
    
    #Delete member from group
    def remove_member_from_group(self,group_id,member_id_to_delete,
                                 remove_date):
        #Delete member from group
        status = self.__groups_members_dal.update_group_member(member_id_to_delete,
                        group_id,{"remove_date":parser.parse(remove_date)})
        return status
    
    #Executed when a group member exits a group by himself
    def self_exit_from_group(self,group_id,
                             member_id_to_exit,exit_date):
        
        #Update membership of member in a group with exit date
        #meaning the membership is no loger active, but
        #still is not totally deleted
        status = self.__groups_members_dal.update_group_member(
            member_id_to_exit,
                        group_id,{"exit_date":parser.parse(exit_date)})
        return status
    

    #Closing a group, meaning making it impossible for its members 
    # to send any more messages 
    def close_group(self,group_id,close_date):

        #close group
        status=self.__groups_dal.update_group(group_id,{"close_date":
                                        parser.parse(close_date)})
        return status
    
    #Delete a group membership of an ex member, that has already exited or 
    # been removed from it before, but the details of his membership 
    # stil were not removed
    def self_delete_member_from_group(self,group_id,member_id):

        status=self.__groups_members_dal.delete_member_from_group(
            group_id,member_id)
        
        #Get all the the group memberships, including those that
        #exited the group or have been removed by the admin of the group
        undeleted_memberships=(
            self.__groups_members_dal.get_all_undeleted_memberships(
            group_id))
        
        #Delete the general detais of group if no member is in the group
        #anymore
        if len(undeleted_memberships)==0:
            self.__groups_dal.delete_group(group_id)
            
                                                                  
        return status