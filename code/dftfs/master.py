# app / __init__.py

import argparse
from flask import Flask, request
import hashlib
import numpy
import requests
from requests.exceptions import Timeout
import time

from threading import Thread
import json

# global variables should always be declared "global" before being used in functions (see index())
port = 0
nb_nodes = 0
nodes_ls = [tuple]
files_locations = []

path_to_addr = {}  # addr need to be [addr1, addr2, addr3], currently just addr
node_size = 1
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
        path_to_addr[notificationData.path] = notificationData.addr
        # put corresponding lent bytes as occupied

    if method == "failure":
        # failure handler
        nAddr = __failure_handler(notificationData.addr)


@app.route('/request/<string:method>')
def request_handler(method):
    # requestData = fictive object containing all info needed to process request
    # responseData = fictive object containing all info needed to craft answer
    requestData = request.json()

    if method == "get":
        # get handler
        responseData.answer = __get_addr(requestData.path)

    elif method == "exists":
        # exist handler
        responseData.answer = __exists(requestData.path)

    elif method == "put":
        # put handler
        responseData.addrs = __duplication_handler(requestData)

    else:  # method = "copy"
    # copy handler
    # src_path, dst_path -> 1st exist == True; 2nd exist == False
    # idem as "put" but fetch bytes from src_path
    # TODO

    return responseData

########################################################################################################################
def __addr_table_access(path):
    return path_to_addr.get(path)

def __exists(path):
    if (__addr_table_access(path) == None):
        return False
    return True

def __get_addr(path):
    addr = __addr_table_access(path)

    if (addr == None):
        return error_addr
    return addr

def __find_space(bytesLen, invalid):
    # bytesLen = bytes length
    # invalid = list of node to be excluded from search)

    # algorithm based on node_spaces list
    # (exclude invalid nodes from this list)
    # return addr with enough space to fit bytesLen
    # if none fit -> return error_addr
    # for now don't care about lent space
    return addr

def __duplication_handler(requestData):
    # find  2 suitable nodes (all nodes != )
    nodes = []
    n = 0
    for n in range(3):
        nAddr = __find_space(requestData.bytesLen, nodes)
        nodes.append(nAddr)
    return nodes

def __failure_handler(addr):
    return 0

# identify all paths which have failed node correspondance
# discard nodeAddr of failed node in path_to_addr dictoinnary

# contact node which has file & ask them for file size for path
# -> or keep info somewhere in a table in master
# nAddr = self__find_space(bytesLen, [])
# ask node to copy file to nAddr (master writes a request)
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
                    response = requests.get("http://localhost:" + str(n[0]) + "/heart", timeout=5)
                except Timeout:
                    lst = list(n)
                    lst[1] = "dead"
                    n = tuple(lst)
                    duplicate_data()  # duplicate
                    continue
                try:
                    data = response.json()
                    print(data)
                    print(data.keys().find('state'))
                    print(data.values())
                except json.decoder.JSONDecodeError:
                    lst = list(n)
                    lst[1] = "dead"
                    n = tuple(lst)
                    duplicate_data()  # duplicate
                    continue
                lst = list(n)
                lst[1] = "alive"
                n = tuple(lst)


# to be implemented
def duplicate_data():
    return "Ok"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('nodes')
    parser.add_argument('flask_port')
    args = parser.parse_args()
    nb_nodes = int(args.nodes)
    port = int(args.flask_port)
    nodes_ls = [(2000, "dead")] * nb_nodes
    for node in range(nb_nodes):
        nodes_ls[node] = (2000 + node, "alive")
    watch = Watchdog()
    watch.start()
    app.run(host="localhost", port=port)
