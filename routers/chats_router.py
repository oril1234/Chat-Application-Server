#Module of all endpoints related to chats in users speak with each other
#using text messages
from flask import Blueprint,jsonify, make_response, request
from BL.chats_bl import ChatsBL

chats = Blueprint('chats', __name__)

#instance of chats business logic
chats_bl=ChatsBL()


#Delete user from chat, meaining the chat will still exist but 
#the user won't see it
@chats.route("/delete_user_from_chat/<chat_id>/<user_id>",
              methods=['DELETE'])
def delete_user_from_chat(chat_id,user_id):
    response=chats_bl.delete_user_from_chat(chat_id,user_id)
    return jsonify(response)

