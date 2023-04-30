from DAL.messages_dal import MessagesDal
from DAL.users_dal import UsersDal
from DAL.users_chats_dal import UsersChatsDal
from DAL.groups_members_dal import GroupsMembersDal
from DAL.groups_dal import GroupsDal
from DAL.chats_dal import ChatsDal
from DAL.blocks_dal import BlocksDal
from BL.groups_bl import GroupsBL
from datetime import datetime, timedelta
from dateutil import parser
from datetime import datetime
import jwt
from flask_bcrypt import Bcrypt
import json
import uuid

#Business logic class of general actions
class GeneralBL:
    def __init__(self):
        #Instance of users chats data layer connected to data base
        self.__users_chats_dal = UsersChatsDal()

        #Instance of users groups data layer connected to data base
        self.__groups_members_dal = GroupsMembersDal()

        #Instance of users data layer connected to data base
        self.__users_dal=UsersDal()

        #Instance of groups data layer connected to data base
        self.__groups_dal=GroupsDal()

        #Instance of chats data layer connected to data base
        self.__chats_dal=ChatsDal()

        #Instance of blocks data layer connected to data base
        self.__blocks_dal=BlocksDal()

        #Instance of messages data layer connected to data base
        self.__messages_dal = MessagesDal()

        #Instance of groups business logic
        self.__groups_bl=GroupsBL()

    #Get the data related to specific user channels which are his chats
    # with at least one message sent and groups, by his email
    def get_user_active_channels_data(self,email):

        #Get all user details in chat
        user_chats=self.__users_chats_dal.get_user_chats_by_user(email)

        #A tuple of data of current user groups memberships. First 
        #item in tuple is all the memberships of the user, and the second
        #one is the ids of only the active memberships - of groups the
        #user did not leave or was removed from by the admin
        user_groups_data=self.__groups_bl.get_user_groups_memberships(
            email)

        #Data of all the channerls of user - chats and groups
        channels=[]

        #Iterating details of user in his chats to format and then 
        #return them
        for user_chat in user_chats:
            curr_chat={}
            curr_chat["user_id"]=email
            chat_id=user_chat["_id"]["chatID"]
            curr_chat["chat_id"]=chat_id

            #General chat data
            chat_data=self.__chats_dal.get_chat(chat_id)

            #ID of the user the current user chats with in the current 
            #chat
            partner_id=user_chat["partnerID"]

            #Full details of partner
            partner=self.__users_dal.get_user(partner_id)
            del partner["password"]
            curr_chat["partner"]=partner

            #Last activity date time in chat, meaning the date time the 
            #last message was sent by any of its 2 participants
            curr_chat["last_activity"]=chat_data["last_activity"]

            #Number of messages sent by the partner of the current user,
            #which the last one did haven't read yet
            curr_chat["unread_messages_number"]=int(
                user_chat["unread_messages_number"])
            
            #Details of blocking of the current user by his partner
            #and/or the other way around
            blocks_data=list(self.__blocks_dal.get_blocks(
                email,partner["_id"]))
            curr_chat["blocks_data"]=list(
                map(lambda block_data:block_data["_id"],blocks_data )
            )

            #Details of messages sent in current chat
            curr_chat["channel_messages"]=(
                
                #self.__messages_dal.get_chat_messages(chat_id)
                    [dict(message,**{'to':partner_id}) 
                    if message["userID"]==email
                    else 
                    dict(message,**{'to':email}) 
                    for message in self.__messages_dal.get_chat_messages(chat_id)
                ]
                )
        
            #Adding currenr channel to returned list if at least
            # one message was sent in current chat            
            if len(curr_chat["channel_messages"])>0:
                channels.append(curr_chat)

        #Iterating details of current user in his group to 
        #format and then return them
        for user_group_membership in user_groups_data[0]:
            curr_group_data={}
            group_id=user_group_membership["_id"]["groupID"]

            #Get general group data
            group_details=self.__groups_dal.get_group(group_id)
            del group_details["_id"]
            group_details["group_name"]=group_details["name"]
            del group_details["name"]
            curr_group_data["group_id"]=group_id
            curr_group_data.update(group_details)
            curr_group_data.update(user_group_membership)
            if "muted" in curr_group_data:
                curr_group_data["unread_messages_number"]=0
            del curr_group_data["_id"]
            curr_group_data["user_id"]=email

            #Memberships details of all members of current group
            group_memberships=(
                self.__groups_members_dal.get_group_memberships(group_id))
            group_members_ids=list(
                map(lambda user_in_group : user_in_group["_id"]["userID"],
                 group_memberships))
            group_members=self.__users_dal.get_specified_users(
                group_members_ids)
            curr_group_data["members"]=group_members

            #Details of messages sent in the group
            curr_group_data["channel_messages"]=list(
                self.__messages_dal.get_group_messages(group_id)
            )
            channels.append(curr_group_data)

        return channels

    #Get the data related to contacts with which the provided user 
    #did not comminicate yet via chats
    def get_user_uncomunicated_contacts(self,email):
        user_chats=self.__users_chats_dal.get_user_chats_by_user(email)

        #Get groups memberships of user in order
        #to use it later to find shared groups with uncommucnicated contacts
        user_groups_memberships=(
        self.__groups_members_dal.get_user_groups_membership(
            email
        ))
        user_groups_ids=list(map(lambda user_group_membership:
                                user_group_membership["_id"]["groupID"],
                                user_groups_memberships))
        
        #Fetching all the details of the users with which the current 
        #user has exchanges messages within chats
        partners_chats=self.__users_chats_dal.get_partners_chats_details(
            list(map(lambda user_chat:user_chat["_id"]["chatID"],
                     user_chats)),
            email
        )
        partners_ids=list(map(lambda partner:partner["_id"]["userID"],
                     partners_chats))
        partners_ids.append(email)


        #Get all uncomunicated contacts
        uncom_contacts=self.__users_dal.get_all_users_except(partners_ids)

        #Creating new chats with uncommunicated contacts
        chats=[]

        #Iterating uncommunicated contacts details in order to format 
        #chats of them and the current user
        for contact in uncom_contacts:
            curr_chat={}
            curr_chat["user_id"]=email
            curr_chat["chat_id"]=str(uuid.uuid4())
            del contact["password"]
            curr_chat["partner"]=contact
            contact_groups_memberships=self.__groups_members_dal.get_user_groups_membership(
            contact["_id"]
            )

            #IDs of groups the current 
            #uncommunicated contact participates in
            contact_group_ids=list(map(lambda contact_group_membership:
                                contact_group_membership["_id"]["groupID"],
                                contact_groups_memberships))
            
            #Shared groups of the current user and the
            #current uncommunucated contact
            shared_groups_ids=set(user_groups_ids).intersection(
                contact_group_ids)
            shared_groups=self.__groups_dal.get_groups_by_ids(
                list(shared_groups_ids))
            curr_chat["shared_groups"]=shared_groups

            #Field that stores the date time the last 
            #message in chat was sent, and since no message was sent
            #it gets the current date time 
            curr_chat["last_activity"]=str(datetime.now())

            #Number of messages that were unread in chat by currrent
            #user which is obviously 0, otherwise uncommunicated contact
            #wouldn't have been uncommunicated
            curr_chat["unread_messages_number"]=0
            curr_chat["channel_messages"]=[]

            #Data of blockings of current user by current uncommunicated contact,
            #and the other way around
            blocks_data=list(self.__blocks_dal.get_blocks(email,contact["_id"]))
            if len(blocks_data)>0:
                curr_chat["blocks_data"]=blocks_data

            chats.append(curr_chat)

        return chats

    



    
 