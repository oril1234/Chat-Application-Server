# Chat Application
This is a server of a chat application. It listens to [React clients](https://github.com/oril1234/Cinema-Management-System-React-Client) for HTTP calls and maintains websocket connection to allow real time updates with them.
The server supports the following actions
1. Send and receive messages in private chats of 2 users, and group chats with multiple participants
2. Create new groups
3. Adding new members to groups
4. Removing members from groups by its admin
5. Self exit from group of a member
6. block and unblock users by others.

The server communicates with Mongo DB where it manages 
the data of users, chats, groups, memberships in groups of users, blocking of users


### Requirements
Python 3.8.+

### Install Requirements
- pip install requests
- pip install pymongo
