#Module of all endpoints related to blocking of users by others in chats
from flask import Blueprint,jsonify, make_response, request
from BL.blocks_bl import BlocksBL

blocks = Blueprint('blocks', __name__)

#instance of blocks business logic
blocks_bl=BlocksBL()

#Update blocked users and their blockers
@blocks.route("/block_user", methods=['POST'])
def block_user():
    block_details=request.json
    response=blocks_bl.block_user(block_details)
    return jsonify(response)

#Cancel blocking of a user
@blocks.route("/unblock_user", methods=['PUT'])
def unblock_user():
    unblock_details=request.json
    response=blocks_bl.unblock_user(unblock_details)
    return jsonify(response)