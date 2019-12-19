# app / __init__.py

import argparse
from flask import Flask, request
import hashlib
import numpy
import requests
from requests.exceptions import Timeout
import time
import random

from threading import Thread
import json

# global variables should always be declared "global" before being used in functions (see index())
port = 0
nb_nodes = 0
nodes_ls = []

path_to_addr = {}  # addr need to be [addr1, addr2, addr3], currently just addr
node_size = 1024
sizes = [node_size] * nb_nodes  # [node_size, node_size, ...]
node_spaces = zip(nodes_ls, sizes)  # [(node1addr, size1), (node2addr,size2), ...]

app = Flask(__name__)


# faut-il rajouter "/<path:name>" après "/notification" pr avoir le path cô ds put_handler ?
@app.route('/notification/<string:method>')
def notification_handler(method):
    # notificationData is a json dict with 'key:value' pairs
    notificationData = request.json
    if method == "put":
        # put handler
        global path_to_addr[notificationData["path"] = notificationData["addr"]
        return 0
    """
    if method == "failure":
        # failure handler
        wAddr = failure_handler(notificationData["addr"])
    """

@app.route('/request/<string:method>')
def request_handler(method):
    # requestData = dictionary containing all info needed to process request
    # responseData = dictionary containing all info needed to craft answer
    requestData = request.json()
    responseData = {}

    if method == "get":
        # get handler
        responseData["gAddr"] = addr_table_access(requestData["path"]) #gAddr = get address

    elif method == "exists":
        # exist handler
        responseData["exist"] = exists(requestData["path"])

    elif method == "put":
        # put handler
        responseData["wAddr"] = duplication_handler(requestData["bytesLen"]) #wAddr = write address

    else:
        responseData["error"] = "unknownRequest"

    return json.dumps(responseData)

########################################################################################################################
def addr_table_access(path):
    return global path_to_addr[path]

def exists(path):
    if (addr_table_access(path) == None):
        return False
    return True

def find_space(bytesLen, invalid):
    # bytesLen = bytes length
    # invalid = list of node to be excluded from search)
    valid = []

    for tuple in global node_spaces:
        if tuple[0] not in invalid:
            if tuple[1] > bytesLen:
                valid.append(tuple[0])
                
    if not valid:
        return None
    return random.choice(valid) # need to make (chosenAddr, size) -> (chosenAddr, size - bytesLen)

def duplication_handler(bytesLen):
    wAddr = []
    invalid = []
    
    for i = 1 to 3
        wAddr.append(find_space(bytesLen, invalid))
        invalid.append(wAddr) #duplicates addresses but not a problem
        
    return wAddr

def failure_handler(addr):
    # identify all paths which have failed node correspondance
    # discard nodeAddr of failed node in path_to_addr dictoinnary

    # contact node which has file & ask them for file size for path
    # -> or keep info somewhere in a table in master
    # nAddr = self__find_space(bytesLen, [])
    # ask node to copy file to nAddr (master writes a request)
    return 0

########################################################################################################################

class Watchdog(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global nodes_ls
        while True:
            time.sleep(3)
            for n in nodes_ls:
                try:
                    response = requests.get("http://localhost:" + str(n) + "/heart", timeout=5)
                except Timeout:
                    """
                    lst = list(n)
                    lst[1] = "dead"
                    n = tuple(lst)
                    duplicate_data()  # duplicate
                    """
                    #call failure_handler(n)
                    continue
                try:
                    data = response.json()
                    print(data)
                    print(data.keys().find('state'))
                    print(data.values())
                except json.decoder.JSONDecodeError:
                    """
                    lst = list(n)
                    lst[1] = "dead"
                    n = tuple(lst)
                    duplicate_data()  # duplicate
                    """
                    #call failure_handler(n)
                    continue

"""
# to be implemented
def duplicate_data():
    return "Ok"
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('nodes')
    parser.add_argument('flask_port')
    args = parser.parse_args()
    #setting of arguments
    """
    nb_nodes = int(args.nodes)
    port = int(args.flask_port)
    nodes_ls = [(2000, "dead")] * nb_nodes
    for node in range(nb_nodes):
        nodes_ls[node] = (2000 + node, "alive")
    """
    nb_nodes = int(args.nodes)
    nodes_ls = [2000] * nb_nodes
    for node in range(nb_nodes):
        nodes_ls[node] = (2000 + node)
    #end of setting argument
    watch = Watchdog()
    watch.start()
    app.run(host="localhost", port=port)
