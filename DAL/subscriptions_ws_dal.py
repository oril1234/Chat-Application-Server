import requests

#Subsriptions data layer class that connects with subscriptions
#web service procided by another server
class SubscriptionsWSDal:
    def __init__(self):
        #URL of subscriptions web service
        self.__url = "http://localhost:5001/subscriptions"

    #Fetching all the subscriptions in the system
    def get_all_subscriptions(self):
        resp = requests.get(self.__url)
        return resp.json()

    #Add new subscription of a movie by a member
    def add_subscription(self,obj):
        resp = requests.post(self.__url,json=obj)
        return resp.json() 
