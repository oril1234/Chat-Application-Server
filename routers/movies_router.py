#Module of all endpoints related to movies in the system

from flask import Blueprint,jsonify, request
from BL.movies_bl import MoviesBL

movies = Blueprint('movies', __name__)

#Movies business logic instance
movies_bl=MoviesBL()

#Fetching all the movies in the system
@movies.route("/", methods=['GET'])
def get_all_movies():
    movies = movies_bl.get_all_movies()
    return jsonify(movies)
    


#Adding new movie to the system
@movies.route("/", methods=['POST'])
def add_movie():
    obj = request.json
    result = movies_bl.add_movie(obj)
    return jsonify(result)


#Update movie details in the system
@movies.route("/<id>", methods=['PUT'])
def update_movie(id):
    obj = request.json
    result = movies_bl.update_movie(id,obj)
    return jsonify(result)


#Delete movie details from the system
@movies.route("/<id>", methods=['DELETE'])
def delete_movie(id):
    result = movies_bl.delete_movie(id)
    return jsonify(result)