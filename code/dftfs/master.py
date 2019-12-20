# app / __init__.py

import argparse
from flask import Flask, request, json
import hashlib
import numpy
import requests
from requests.exceptions import Timeout
import time
import random
from threading import Thread
import json

# global variables should always be declared "global" before being used in functions (see index())
master_addr = 0
nb_nodes = 0
nodes_ls = []

path_to_addr = {}  # addr need to be [addr1, addr2, addr3], currently just addr
node_size = 1024
sizes = [node_size] * nb_nodes  # [node_size, node_size, ...]
node_spaces = zip(nodes_ls, sizes)  # [(node1addr, size1), (node2addr,size2), ...]
fault_tol = 3

app = Flask(__name__)


# faut-il rajouter "/<path:name>" après "/notification" pr avoir le path cô ds put_handler ?
@app.route('/notification/<string:method>', methods=['POST'])
def notification_handler(method):
    # notification_data is a json dict with 'key:value' pairs
    notification_data = request.json()
    if method == "put":
        # put handler
        global path_to_addr
        path_to_addr[notification_data["path"]] = notification_data["addr"]
        return 0
    """
    if method == "failure":
        # failure handler
        waddr = failure_handler(notification_data["addr"])
    """


@app.route('/request/<string:method>', methods=['POST'])
def request_handler(method):
    # request_data = dictionary containing all info needed to process request
    # response_data = dictionary containing all info needed to craft answer
    # request_data = request.json()
    request_data = request.form
    print("in master")
    print(request_data)
    response_data = {}

    if method == "get":
        # get handler
        response_data["gaddr"] = addr_table_access(request_data["path"])  # gaddr = get address

    elif method == "exists":
        # exists handler
        response_data["exists"] = exists(request_data["path"])

    elif method == "put":
        # put handler
        response_data["waddr"] = duplication_handler(request_data["bytes_len"])  # waddr = write address

    else:
        response_data["error"] = "unknownRequest"

    return json.dumps(response_data)


########################################################################################################################
def addr_table_access(path):
    global path_to_addr
    return path_to_addr.get(path)


def exists(path):
    if addr_table_access(path) is None:
        return False
    return True


def find_space(bytes_len, invalid):
    # bytes_len = bytes length
    # invalid = list of node to be excluded from search)
    valid = []
    global node_spaces

    for tuple_ in node_spaces:
        if tuple_[0] not in invalid:
            if tuple_[1] > bytes_len:
                valid.append(tuple_[0])

    if not valid:
        return None
    return random.choice(valid)  # need to make (chosenAddr, size) -> (chosenAddr, size - bytes_len)


def duplication_handler(bytes_len):
    waddr = []
    invalid = []

    for i in range(fault_tol):
        waddr.append(find_space(bytes_len, invalid))
        invalid.append(waddr)  # duplicates addresses but not a problem

    return waddr


def failure_handler(addr):
    # identify all paths which have failed node correspondance
    # discard nodeAddr of failed node in path_to_addr dictoinnary

    # contact node which has file & ask them for file size for path
    # -> or keep info somewhere in a table in master
    # nAddr = self__find_space(bytes_len, [])
    # ask node to copy file to nAddr (master writes a request)
    return addr


########################################################################################################################

class Watchdog(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global nodes_ls
        while True:
            for n in nodes_ls:
                try:
                    response = requests.get("http://localhost:" + str(n) + "/heart", timeout=5)
                except Timeout:
                    """
                    lst = list(n)
                    lst[1] = "dead"
                    n = tuple_(lst)
                    duplicate_data()  # duplicate
                    """
                    # call failure_handler(n)
                    continue
                try:
                    data = response.json()
                except json.decoder.JSONDecodeError:
                    """
                    lst = list(n)
                    lst[1] = "dead"
                    n = tuple_(lst)
                    duplicate_data()  # duplicate
                    """
                    # call failure_handler(n)
                    continue
            time.sleep(300)


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
    # setting of arguments
    """
    nb_nodes = int(args.nodes)
    port = int(args.flask_port)
    nodes_ls = [(2000, "dead")] * nb_nodes
    for node in range(nb_nodes):
        nodes_ls[node] = (2000 + node, "alive")
    """
    nb_nodes = int(args.nodes)
    master_addr = int(args.flask_port)
    nodes_ls = [2000] * nb_nodes
    for node in range(nb_nodes):
        nodes_ls[node] = (2000 + node)
    # end of setting argument
    watch = Watchdog()
    watch.start()
    app.run(host="localhost", port=master_addr)
