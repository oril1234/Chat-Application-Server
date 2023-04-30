#Module of all endpoints related to groups 
#of users who can chat with each other
from flask import Blueprint,jsonify, make_response, request
from BL.groups_bl import GroupsBL

groups = Blueprint('groups', __name__)

#instance of groups business logic
groups_bl=GroupsBL()



#Adding new group to system
@groups.route("/new_group", methods=['POST'])
def add_group():
    group=request.json
    response=groups_bl.create_group(group)

    #Executed if new group creation succeeded
    if response is not None and len(response)>0:
        return make_response({"message" : "Group successfully created"},200)

    #Executed if new group creation failed
    return make_response({"error" :"Error occured creating new group"
        },500)

#Get shared groups between 2 users
@groups.route("/shared_groups/<user_id1>/<user_id2>", methods=['GET'])
def get_shared_groups(user_id1,user_id2):
    response=groups_bl.get_shared_groups_by_user_ids(user_id1,user_id2)
    return make_response({"data" : response },200)

#Closing a group by its admin, meaning no one can send messages
#anymore in it
@groups.route("/close_group", methods=['PUT'])
def close_group():
    close_data=request.json
    response=groups_bl.close_group(close_data["group_id"],close_data["close_date"])
    return jsonify(response)

#Adding new group members to system
@groups.route("/new_group_members/<group_id>", methods=['PUT'])
def update_group_members(group_id):
    members=request.json
    response=groups_bl.add_new_group_members(group_id,members)

    #Executed if new group members addition succeeded
    if response is not None and len(response)>0:
        return make_response({"message" : "Group members added successfully created"},200)

    #Executed if new group members addition failed
    return make_response({"error" :"Error occured adding new group members"
        },500)


#Cancel membership of group member by group admin
@groups.route("/remove_member_from_group/<group_id>/<member_id>",
               methods=['PUT'])
def remove_group_member(group_id,member_id):
    remove_date=request.json
    response=groups_bl.remove_member_from_group(group_id,member_id,
                                                remove_date)
    return jsonify(response)

#Delete completely membership of a user in a group after 
# he has already exited or been removed beforehand
@groups.route("/self_delete_member_from_group/<group_id>/<member_id>",
               methods=['DELETE'])
def self_delete_member_from_group(group_id,member_id):
    response=groups_bl.self_delete_member_from_group(group_id,member_id)
    return jsonify(response)

#Self exit of a group member from group
@groups.route("/group_member_exit/<group_id>/<member_id>", methods=['PUT'])
def group_member_exit(group_id,member_id):
    exit_date=request.json
    response=groups_bl.self_exit_from_group(group_id,member_id,exit_date)

    return jsonify(response)