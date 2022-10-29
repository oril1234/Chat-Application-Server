from DAL.movies_ws_dal import MoviesWSDal

#Business logic class of the movies in the system
class MoviesBL:
    def __init__(self):

        #Instance of the movies data layer that connects
        # with a movies web service provided by another server
        self.__movies_ws_dal = MoviesWSDal()
        
    #Fetching all the movies 
    def get_all_movies(self):
       movies = self.__movies_ws_dal.get_all_movies()
       return movies

    #Add new movie to the system
    def add_movie(self,obj):
        status = self.__movies_ws_dal.add_movie(obj)
        return status

    #Update an existing movie in the system
    def update_movie(self,id,obj):
         status = self.__movies_ws_dal.update_movie(id,obj)
         return status

    #Delete movie by his id
    def delete_movie(self,id):
        status = self.__movies_ws_dal.delete_movie(id)
        return status