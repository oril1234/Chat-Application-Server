from DAL.blocks_dal import BlocksDal


#Business logic of blocking other users, meaning they 
#can't send messages to them via private chat
class BlocksBL:
    def __init__(self):



        #Instance of blocks data layer connected to data base
        self.__blocks_dal=BlocksDal()
 
    #Adding new data regarding a user blocking another oner
    def block_user(self,block_data):
        status=self.__blocks_dal.block_user(block_data)
        return status
    
    #Cancel blocking of user by another one 
    def unblock_user(self,unblock_data):
        status=self.__blocks_dal.unblock_user(unblock_data)
        return status