
#Module of all endpoints retlated to subscriptions to moviess 
#for the members registered in the system

from flask import Blueprint,jsonify, request
from BL.subscriptions_bl import SubscriptionsBL

subscriptions = Blueprint('subscriptions', __name__)

#Subscriptions business logic instance
subscriptions_bl=SubscriptionsBL()

#Fetching all the subscriptions in the system
@subscriptions.route("/", methods=['GET'])
def get_all_subscriptions():
    subscriptions = subscriptions_bl.get_all_subscriptions()
    return jsonify(subscriptions)
    

#Adding new subscription to the system
@subscriptions.route("/", methods=['POST'])
def add_subscription():
    obj = request.json
    result = subscriptions_bl.add_subscription(obj)
    return jsonify(result)

