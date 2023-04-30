#Module of all endpoints related to messages being sent 
#between users in chats and groups
from flask import Blueprint,jsonify, make_response, request
from BL.messages_bl import MessagesBL

messages = Blueprint('messages', __name__)

#instance of messages business logic
messages_bl=MessagesBL()


#Endpoint for adding new message to db
@messages.route("/new_message", methods=['POST'])
def add_new_messages():
    obj = request.json
    result = messages_bl.add_message(obj)
    return jsonify(result)

#Endpoint for reading unread messages by user in a chat
@messages.route("/read_chat_user_unread_messages", methods=['PUT'])
def read_chat_user_unread_messages():
    obj = request.json
    result = messages_bl.read_user_messages_in_chat(obj["user_id"],
                                    obj["chat_id"])
    return jsonify(result)

#Endpoint for readomg unread messages by user in a group
@messages.route("/read_group_member_unread_messages", methods=['PUT'])
def read_group_member_unread_messages():
    obj = request.json
    result = messages_bl.read_group_member_unread_messages(obj["member_id"],
                                    obj["group_id"])
    return jsonify(result)