

port = 0
nodes_ls = []
node_size # max quantity of bytes a node contains


#@ route (request)
responseData = master.request_handler(requestData)
#craft response & send back

#@route (notification)
master.notification_handler(notificationData)


class Master:
    
    port
    path_to_addr # addr need to be [addr1, addr2, addr3], currently just addr
    node_spaces
    
    def __init__(self, port, nodes_ls, node_size):
    
        self.port = port
        
        self.path_to_addr = {}
        
        nb_nodes = len(node_ls)
        
        sizes = [node_size] * nb_nodes # [node_size, node_size, ...]
        
        self.node_spaces = zip(node_ls, sizes) # [(node1addr, size1), (node2addr,size2), ...]
        
    def request_handler(self,requestData):
    # requestData = fictive object containing all info needed to process request
    # responseData = fictive object containing all info needed to craft answer
        
        if(requestData.type == "get")
            #get handler
            responseData.answer = self.__get_addr(requestData.path)
        if(requestData.type == "exists")
            #exist handler
            responseData.answer = self.__exists(requestData.path)
        if(requestData.type == "put")
            #put handler
            responseData.addrs = self.__duplication_handler(requestData)
            
        if(requestData.type == "copy")
            #copy handler
            #src_path, dst_path -> 1st exist == True; 2nd exist == False
            #idem as "put" but fetch bytes from src_path
            #TODO
        return ResponseData
        
    def __addr_table_access(self, path):
    
        return path_to_addr.get(path)
        
    def __exists(self, path):
        if(__addr_table_access(path) == None):
            return False
        return True
        
    def __get_addr(self, path):
    
        addr = __addr_table_access(path)
        
        if(addr == None):
            return error_addr
        return addr
        
    def __find_space(self, bytesLen, invalid): 
    # bytesLen = bytes length
    # invalid = list of node to be excluded from search)
        
        #algorithm based on node_spaces list 
        #(exclude invalid nodes from this list)
        #return addr with enough space to fit bytesLen
            #if none fit -> return error_addr
        #for now don't care about lent space
        return addr
      
    def __duplication_handler(self, requestData):
    
        #find  2 suitable nodes (all nodes != )
        nodes = []
        n = 0
        for n in range(3):
            nAddr = __find_space(requestData.bytesLen, nodes)
            nodes.append(nAddr)
        return nodes
    
    def notification_handler(self, notificationData):
        
        if(notificationData.type == "put")
            #put handler
            self.path_to_addr[notificationData.path] = notificationData.addr
            #put corresponding lent bytes as occupied
    
        if(notificationData.type == "failure")
            #failure handler
            nAddr = self.__failure_handler(notificationData.addr)
    
    def __failure_handler(self, addr):
        
        # identify all paths which have failed node correspondance
        # discard nodeAddr of failed node in path_to_addr dictoinnary 
        
        # contact node which has file & ask them for file size for path
            #-> or keep info somewhere in a table in master
        # nAddr = self__find_space(bytesLen, [])
        # ask node to copy file to nAddr (master writes a request)
        
if __name__ == "__main__":

    master = Master(port, node_ls, node_size)
    #app.run()