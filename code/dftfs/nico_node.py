

master_ip

#@ route (client request)
responseData = node.client_handler(requestData)
#craft response & send back

#@ route (node request)
responseData = node.node_handler(requestData)
#craft response & send back

class Node:
    
    master_ip
    node_addr
    path_to_bytes
    
    def __init__(self,node_addr, master_ip):
        
        self.master_ip = master_ip
        self.path_to_file = {}
        
    def client_handler(self, requestData):
    # requestData = fictive object containing all info needed to process request
    # responseData = fictive object containing all info needed to craft answer
    
        masterAnswer = self.__request_master(requestData)

        if(requestData.type == "exists")
            #exist handler
            responseData = masterAnswer.exists
        if(requestData.type == "get")
            #get handler
            if(masterAnswer.addr != self.addr):
                nodeAnswer = __request_node("get",requestData, masterAnswer.addr)
                responseData = nodeAnswer.bytes
            else:
                requestData.bytes = path_to_bytes[requestData.path]
        if(requestData.type == "put")
            #put handler
            if(masterAnswer.addr != self.addr):
                nodeAnswer = __request_node("put",requestData, masterAnswer.addr1) # duplicates
                responseData = nodeAnswer.result # aka success or failure
                # duplicates 2 more "put" request_node !!!!!
                # for duplicates, discard nodeAnswers
                #also always check if masterAnswer.addr != self.addr
            else:
                path_to_bytes[requestData.path] = requestData.bytes
                self.__notifyMaster(requestData.path, self.addr)
        if(requestData.type == "copy")
            #copy handler
            if(masterAnswer.addr != self.addr1):
                bytes = __request_node("get",requestData, masterAnswer.addr1)
            else:
                bytes = path_to_bytes[requestData.path]
            nodeAnswer = = __request_node("put", bytes, masterAnswer.addr2)
            responseData = nodeAnswer.result # aka success or failure
            # duplicates 2 more "put" request_node !!!!!
            # for duplicates, discard nodeAnswers
            #also always check if masterAnswer.addr != self.addr
        return ResponseData
    
    def __request_master(requestData):
    
        #craft a specific master request using requestData
        #wait for master response
        return masterAnswer
        
    def __request_node(requestType,requestData, nodeAddr):
        
        #craft "requestType" node_request to node at nodeAddr
        #wait for response
        return nodeAnswer
        
    def node_handler(requestData):
    # requestData = fictive object containing all info needed to process request
    # responseData = fictive object containing all info needed to craft answer    
        
        if(requestData.type == "get")
            responseData.bytes = path_to_bytes[requestData.path]
        if(responseData.type == "put")
            path_to_bytes[requestData.path] = requestData.bytes
            self.__notifyMaster(requestData.path, self.addr)
            responseData.result = True
        return responseData
        
    def __notifyMaster(path,addr)
    
        # craft a notification to the master
        # so that master can update its path_to_addr table
        # no response from master -> no waiting
    
if __name__ == "__main__":

    node = node(node_addr ,master_ip)
    #app.run()
    