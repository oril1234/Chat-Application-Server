from DAL.messages_dal import MessagesDal
from DAL.users_dal import UsersDal
from DAL.users_chats_dal import UsersChatsDal
from DAL.groups_members_dal import GroupsMembersDal
from DAL.groups_dal import GroupsDal
from DAL.chats_dal import ChatsDal
from dateutil import parser

#Business logic class of messages sent between users in chats and groups
class MessagesBL:
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

        #Instance of messages data layer connected to data base
        self.__messages_dal = MessagesDal()


    #Add new message to db after sent by a user
    def add_message(self,message):
        sender_id=message["userID"]
        #Messages sender details
        sender_data=self.__users_dal.get_user(sender_id)
        

        #Format message date before adding message to db
        message["sentAt"]= parser.parse(message["sentAt"])
        
        #Sender username
        message["username"]=sender_data["username"]
        
        
        status = self.__messages_dal.add_message(message)
        
        #Executed if message was sent in a chat
        if "chatID" in message:

            #ID of user to which the messsage is sent
            receiver_id=message["to"]
            chat_id=message["chatID"]

            #Get general chat details
            chat=self.__chats_dal.get_chat(message["chatID"])

            #Executed if until the message was sent the sender and the
            #reciever of the message haven't sent messages to each other
            if chat is None:
                self.__chats_dal.add_chat({"_id":chat_id,
                                "last_activity":message["sentAt"]})
            
            #Executed if the current message is not the first to be sent
            #between the two users
            else:
                self.__chats_dal.update_chat(chat_id,
                {"last_activity":message["sentAt"]})

            #Executed if there are no details of the message 
            #sender in chat
            if (
                self.__users_chats_dal.get_chat_user(sender_id,chat_id) 
                is None):   
                self.__users_chats_dal.add_user_to_chat({
                    "_id":{"userID":sender_id,"chatID":chat_id},
                    "partnerID":receiver_id,
                    "unread_messages_number":0})

            #Executed if there are no details of the message 
            #receiver in chat
            if (
                self.__users_chats_dal.get_chat_user(receiver_id,chat_id) 
                is None):   
                self.__users_chats_dal.add_user_to_chat({
                    "_id":{"userID":receiver_id,"chatID":chat_id},
                    "partnerID":sender_id,
                    "unread_messages_number":1})
            
            #Executed if there already details of the receiver in the chat
            else:
                self.update_chat_user_unread_messages(receiver_id,chat_id)


        #Executed if message was sent within a group
        else:
            group_id=message["groupID"]
            self.__groups_dal.update_group(group_id,
            {"last_activity":message["sentAt"]})
            status=self.update_group_members_unread_messages(sender_id,
                                                             group_id)
        return status
    
    #Update the number of unread messages in a specific chat by 
    #a specific user
    def update_chat_user_unread_messages(self,user_id,chat_id):

        #Get details of the user in the chat
        chat_user=self.__users_chats_dal.get_chat_user(user_id,chat_id)
        status=None

        #Executed if details of the user in the chat exists
        if chat_user is not None:
            curr_unread_messages_num=chat_user["unread_messages_number"]
            curr_unread_messages_num=curr_unread_messages_num+1
            chat_user["unread_messages_number"]=curr_unread_messages_num
            status=self.__users_chats_dal.update_chat_user(
                user_id,chat_id,chat_user)
        return status
    
    #Reading unread messages in a acht by user, meaning the fiels of
    #the unread messages number will be updated to 0
    def read_user_messages_in_chat(self,user_id,chat_id):
        
        #Get details of the user in the chat
        chat_user=self.__users_chats_dal.get_chat_user(user_id,chat_id)
        status=None

        #Executed if details of the user in the chat exists
        if chat_user is not None:
            chat_user["unread_messages_number"]=0
            status=self.__users_chats_dal.update_chat_user(
                user_id,chat_id,chat_user)
        return status        

    #Update the number of unread messages in a specific group by a
    # all the members after one of them is sending message in it
    def update_group_members_unread_messages(self,sender_id,group_id):
        
        #iterating all the group members in order to update the number of
        #unread messages for each and every one them after a new message
        #was sent in the group
        for group_member in (
            self.__groups_members_dal.get_group_memberships(
         group_id)):
            
            #Update current member as long he's not the sender
            #of the message
            if group_member["_id"]["userID"]!=sender_id:
                curr_unread_messages_num=(
                group_member["unread_messages_number"])
                group_member["unread_messages_number"]=(
                curr_unread_messages_num+1)
                self.__groups_members_dal.update_group_member(
                    group_member["_id"]["userID"],group_id,group_member)
        return "updated"
    
    
    
    #Read all unread messages of a user in a chat
    def read_group_member_unread_messages(self,member_id,group_id):
        
        #Membership details of user
        group_membership=(
            self.__groups_members_dal.get_group_membership(
            member_id,group_id))
        
        #Updating number of unread messages to 0
        group_membership["unread_messages_number"]=0 
        status=self.__groups_members_dal.update_group_member(member_id,
                                    group_id,group_membership)
        return status
    
 