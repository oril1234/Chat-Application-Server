
#Module of all endpoints related to members (people who can
# subscribe to movies)

from flask import Blueprint,jsonify, request
from BL.members_bl import MembersBL

members = Blueprint('members', __name__)

#Members business logic instance
members_bl=MembersBL()

#Fetching all members in the system
@members.route("/", methods=['GET'])
def get_all_members():
    members = members_bl.get_all_members()
    return jsonify(members)
    

#Adding new member to the system
@members.route("/", methods=['POST'])
def add_member():
    obj = request.json
    result = members_bl.add_member(obj)
    return jsonify(result)


#Update member details by his id
@members.route("/<id>", methods=['PUT'])
def update_member(id):
    obj = request.json
    result = members_bl.update_member(id,obj)
    return jsonify(result)


#Delete member details by his id
@members.route("/<id>", methods=['DELETE'])
def dlelete_member(id):
    result = members_bl.delete_member(id)
    return jsonify(result)