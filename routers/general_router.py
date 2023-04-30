#Module of all endpoints related to general actions
from flask import Blueprint,jsonify, make_response, request
from BL.general_bl import GeneralBL
from BL.users_bl import UsersBL

general = Blueprint('general', __name__)

#instance of general business logic
general_bl=GeneralBL()

#instance of users business logic
users_bl=UsersBL()

#Fetching all the data of the user's communicated channels, meaning chats
#in which at least one message was sent and his groups
@general.route("/", methods=['GET'])
def get_user_communicated_channels_data():
    #JWT
    token = request.headers.get("x-access-token")
    token_data=users_bl.decode_token(token)

    email=token_data["userid"]

    channels_data=general_bl.get_user_active_channels_data(email)

    return make_response({"data" : channels_data },200)

#Fetching all the data related to users the current user has no
# communication with ( meaning he still did not exchange messages
#with them)
@general.route("/uncommunicated_contacts", methods=['GET'])
def get_user_uncommunicated_contacts():
    #JWT
    token = request.headers.get("x-access-token")
    token_data=users_bl.decode_token(token)

    email=token_data["userid"]

    contacts_data=general_bl.get_user_uncomunicated_contacts(email)

    return make_response({"data" : contacts_data },200)