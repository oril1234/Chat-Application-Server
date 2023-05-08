# Chat Application
This is a server of a chat application. It listens to [React clients](https://github.com/oril1234/Cinema-Management-System-React-Client) for HTTP calls and maintains websocket connection to allow real time updates with them.
The server supports the following actions
1. Send and receive messages in private chats of 2 users, and group chats with multiple participants
2. Create new groups
3. Adding new members to groups
4. Removing members from groups by its admin
5. Self exit from group of a member
6. block and unblock users by others.

The server consists of 4 layers:
1. Main - The module that is the first to receive API calls. It communicates using both HTTP and
websocket protocols.
2. Routes layer - The modules the HTTP requests are referred to from the main module
3. Business Logic Layer - The modules in which the HTTP requests are processed, and then directed to the data access layers.
4. Data access layers - The modules that are called by the business logic modules in order to directly connect with Mongo Data base and JSON place holder web service

The server communicates with Mongo DB where it manages 
the data of users, chats, groups, memberships in groups of users, blocking of users


Below is the architecture of the server as described above:
![_דיאגרמה ללא שם_ drawio (2)](https://user-images.githubusercontent.com/49225452/236948805-626c4531-8557-418e-9f23-d19bd42e84d5.png)




### Requirements
Python 3.8.+

### Install Requirements
- pip install requests
- pip install pymongo
