# Cinema-Main-Server
This is the main server, which is one of 2 servers of a cinema management system. It provides 5 web services:
1. Movies web service that handles all the movies shown in the cinema 
2. Members web service for people who subscribe to movies by the cinema employees which are the users of the system 
3. Web service of subscripttions of members to movies
4. Web service of the users of the system that when logged in, can perform variety of actions like adding new movies. new members, update, and delete them, as well as adding subscriptions of movies by members, all depending on the permissions the system admin has granted them.
5. Web service of authrntication for login and sign up of users

The server communicates with 4 data sources
1. Mongo Data base collection of users used to store their credentials - usernames and passwords
2. JSON file of those users with their personal details like first name, last name, email, and the amount of time in minutes they are allowed to stay logged in to the system
3. JSON file of those users permissions - all the actions they are allowed to do, as determined by the system admin
4. Subscriptions server of the system which provides 3 web services: members, movies and subscriptions. For more details [click the link](https://github.com/oril1234/Cinema-Management-System-Subscriptions-Flask-Server).

The server consists of 4 layers:
1. Main - The module that is the first to receive API calls
2. Routes layer - The modules the API calls are refered to from the main module
3. Business Logic Layer - The modules called by the routers in which the API calls are processed, and then directed to the data layers.
4. Data layers - The modules that are called by the business logic modules in order to directly connect with Mongo Data base, JSON files, and the subscriptions server


Below is the architecture of the server as described above:
![Main Server Diagram](https://user-images.githubusercontent.com/49225452/198899750-fa0dcec6-700b-433b-9c3a-3861167a4bb4.png)

### Requirements
Python 3.8.+

### Install Requirements
- pip install requests
- pip install pymongo

