from DAL.subscriptions_ws_dal import SubscriptionsWSDal
from bson import ObjectId

#Subsriptions (Orders of movies by members) business logic class 
class SubscriptionsBL:
    def __init__(self):

        #Instance of the subsriptions data layer that connects
        # with a subsriptions web service provided by another server
        self.__subscriptions_ws_dal = SubscriptionsWSDal()        

    #Fetching all the subscriptions in the system
    def get_all_subscriptions(self):
       subscriptions = self.__subscriptions_ws_dal.get_all_subscriptions()
       return subscriptions

    #Adding new subscription of movie by a member
    def add_subscription(self,obj):
        status = self.__subscriptions_ws_dal.add_subscription(obj)
        return status


