from pymongo import MongoClient
from bson import ObjectId
import requests

#Data layer class that connects with a web service of movies
#provided by another server
class MoviesWSDal:
    def __init__(self):

        #URL of movies web service
        self.__url = "http://localhost:5001/movies"

    #Fetching all the movies in the system
    def get_all_movies(self):
        resp = requests.get(self.__url)
        return resp.json()

    #Adding new movie to the system
    def add_movie(self,obj):
        resp = requests.post(self.__url,json=obj)
        return resp.json() 

    #Updating an existing movie ddetails
    def update_movie(self,id,obj):
        resp = requests.put(self.__url+"/"+id,json=obj)
        return resp.json()

    #Delete a movie by his id
    def delete_movie(self,id):
        resp = requests.delete(self.__url+"/"+id)
        return resp.json()