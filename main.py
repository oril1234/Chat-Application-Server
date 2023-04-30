#Main module of chat application server
from flask import Flask, make_response, request
from routers.users_router import users
from routers.general_router import general
from routers.messages_router import messages
from routers.groups_router import groups
from routers.chats_router import chats
from routers.blocks_router import blocks
from flask_cors import CORS
import json
from bson import ObjectId
from flask_socketio import SocketIO, emit,send,join_room, leave_room
from BL.users_bl import UsersBL
from datetime import timedelta
from dateutil import parser

#First Flast setup
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.url_map.strict_slashes = False


#Executed on every HTTP request before it's routed 
#to the corresponding route
@app.before_request
def check_token():

    #Instance of authentication business logic class
    users_bl=UsersBL()
    #Executed only if the sent request is not of type options and the 
    # rquest is not related to authentication (login or sign up of user)
    if (request.method!="OPTIONS" and "/login" not in request.url
        and "/signup" not in request.url):
        
        #Executed if the user added to request headers the JWT
        if request.headers and request.headers.get('x-access-token'):
            #The JWT
            token = request.headers.get('x-access-token')
            
            #Checking the JWT is valid and if not sending error response 
            exists = users_bl.verify_token(token)
            
            if exists is None:
                return make_response({"error" : "Not authorized"},401)
        
        #Executed if user did not send JWT
        else:
            
            return make_response({"error" : "No token provided"},401)
        
#Registering all API calls related to users
app.register_blueprint(users, url_prefix="/users")

#Registering all API calls related to geneal actions
app.register_blueprint(general, url_prefix="/general")

#Registering all API calls related to messages
app.register_blueprint(messages, url_prefix="/messages")

#Registering all API calls related to chats
app.register_blueprint(chats, url_prefix="/chats")

#Registering all API calls related to groups
app.register_blueprint(groups, url_prefix="/groups")

#Registering all API calls related to blocks of users
app.register_blueprint(blocks, url_prefix="/blocks")


#Create websocket connection to the server in order to allow real time
#updates between different clients
socketio = SocketIO(app,cors_allowed_origins="*")

#A dictionary of clients that are currently connected to the server via
#the websocket connection. Each connected client appears twice in the
#dictionay: 1. With the session id as key and the user id of the 
#connected client as the value 2. With the the user id of the 
#connected client as key and the session id of the 
#as the value  
online_users={}

#Triggered when a client diconnect from the websocker 
#connection with the server
@socketio.on('disconnect')
def disconnect():
    user_by_session_id=None
    session_id_by_user=None

    #Executed if session id of the client that is disconnection
    #is in the dictionary
    if request.sid in online_users:
        #Fetching user id of disconnected client using the session
        user_by_session_id=str(online_users[request.sid])

    if user_by_session_id is not None:
        #Fetching session id by user id of disconnected client
        session_id_by_user=str(online_users[user_by_session_id])
        #Deleting the entry its key is the user id, and 
        # the value is session id
        del online_users[user_by_session_id]

        if session_id_by_user is not None:
            #Deleting the entry its key is the session id, and 
            # the value is user id
            del online_users[session_id_by_user]

        #Notifying other users connected from other client,
        #with which the disconnected client has chats with
        #of the disconnection
        emit("user-logged-out",user_by_session_id
        ,broadcast=True,skip_sid=request.sid)

#Storing data of a client that just connected
@socketio.on("add-user")
def add_user(data):

    #Check if user email appears as a key in the online users dictionary
    #to tackle the case in which a client reconnects after
    #unexpected diconnection, and if he does, delete his previous
    #entries
    if data["user_email"] in online_users:
        previous_session_id=online_users[data["user_email"]]
        del online_users[previous_session_id]
        del online_users[data["user_email"]]

    #Update dictinary with new connection details of client    
    online_users[data["user_email"]]=request.sid
    online_users[request.sid]=data["user_email"]

    #A dictionary of the statuses of all the chat partners of the current
    #client. The key is the user id of the partner, and the value is
    #a boolean that says whether or not the this partner is connected
    #to server
    users_connection_status={}

    #patners session ids  of connected clients
    users_session_ids=[]

    if "partners_ids" in data:
        for partner_id in data["partners_ids"]:

            #Executed if patner is connected
            if partner_id in online_users:
                users_connection_status[partner_id]=True
                users_session_ids.append(online_users[partner_id])

            #Executed if patner is not connected
            else:
                users_connection_status[partner_id]=False

        #Notify current client of all of his chats partners that
        #are currently connected
        socketio.emit("receive-users-connections-statuses",
                      users_connection_status,to=request.sid)
        
        #Notify all the chats partners of current client 
        #that he's just connected
        socketio.emit("new-user-logged-in",
                      data["user_email"],to=users_session_ids)
        

#Triggered when a new client is connecting in order to add him to groups
#of which he's a member using flask socket.io rooms 
@socketio.on("join_groups")
def join_groups(groups):
    for group in groups:
        join_room(group)

#Function to add new members to group by admin
def add_new_members_to_group(group_data,members):
        for member in members:
            curr_session=(online_users[member["_id"]] if 
            member["_id"] in online_users else None)
            if curr_session is not None:
                socketio.server.enter_room(curr_session,group_data["group_id"])

#Triggered when a new group is created by its admin and adding its
#members to flask socket.io rooms
@socketio.on("create-new-group")
def create_group(group_data):
    if "group_id" in group_data:
        join_room(group_data["group_id"])
    add_new_members_to_group(group_data,group_data["members"])

    #Notify each and every one of the new members of their addion
    #to the group
    emit("added-to-group",group_data,
        room=group_data["group_id"],broadcast=True,skip_sid=request.sid) 
    
#Triggered when a group admin closes the group, meaning the group
#is not active anymore, and messages cannot be sent.
#The users are notified of the closure.
@socketio.on("close-group")
def close_group(closure_data):
    emit("notify-group-closure",closure_data,room=closure_data["group_id"],
        broadcast=True,skip_sid=request.sid)
    leave_room(closure_data["group_id"])

#Add new members to group by admin
@socketio.on("add-new-group-members")
def add_new_member_to_group(data):
        group_data=data["group_data"]
        new_members=data["members"]

        add_new_members_to_group(group_data,new_members)

        #Notifying each and every one of the new members of
        #their addition to group
        for member in new_members:
            if member["_id"] in online_users:
                to_session_id=online_users[member["_id"]]
                emit("added-to-group",group_data,to=to_session_id) 

#Triggered when admin removes a member from the group
@socketio.on("remove-group-member")
def remove_group_member(removal_data):
        member_id=removal_data["member_id"]
        group_id=removal_data["group_id"]

        session_id=(online_users[member_id] if 
        member_id in online_users else None)

        if session_id is not None:
            socketio.server.leave_room(session_id,group_id)
            #Notify user of his removal
            emit("removed-from-group",removal_data,
                to=session_id)

#Triggered when a message is sent from one user to another
#in a chat or wwithin a group
@socketio.on("send-message")
def send_message(data):
    #Format message date time
    data["sentAt"]=str(parser.parse(data["sentAt"])+timedelta(hours=3))
    
    #Executed if message was sent in a group
    if "groupID" in data:
        #Notifying group members of the new message
        emit("receive-message",data,room=data["groupID"],
        broadcast=True,skip_sid=request.sid)
    
    #Executed if message was sent in a chat between 2 users
    else:
        if data["to"] in online_users:
            to_session_id=online_users[data["to"]]
            #Notifying chat partner of the new message
            socketio.emit("receive-message",data,to=to_session_id)

#Triggered when a user is blocked by another one 
@socketio.on("block-user")
def block_user(block_data):

    #Notifying the user that is blocked of the blocking if
    #he's connected to server
    if block_data["blocked_id"] in online_users:
        to_session_id=online_users[block_data["blocked_id"]]
        socketio.emit("blocked",block_data,to=to_session_id)

#Triggered when a user blocking by another one is cancelled
@socketio.on("unblock-user")
def unblock_user(unblock_data):
    if unblock_data["unblocked_id"] in online_users:
        to_session_id=online_users[unblock_data["unblocked_id"]]

        #Notify unblocked user of his unblocking
        socketio.emit("unblocked",unblock_data,to=to_session_id)
   

if __name__ == '__main__':
    socketio.run(app,debug=True,host="0.0.0.0",port=5000)







