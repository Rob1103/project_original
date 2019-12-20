# app / __init__.py

import argparse
from flask import Flask, request, json
import hashlib
import numpy
import requests
import time
from threading import Thread
import json

# global variables should always be declared "global" before being used in functions (see index())
master_addr = 1024

node_addr = 0
path_to_bytes = {}

app = Flask(__name__)


###################################################################################################

def request_master(request_data, type_):
    return requests.post(url="http://localhost:" + str(master_addr) + "/request/" + type_, data=request_data).json()


def request_node(gaddr, request_data, type_):
    return json.dumps(requests.post(url="http://localhost:" + gaddr + "/node/" + type_, data=request_data))


def notify_master(notification_data):
    return json.dumps(
        requests.post(url="http://localhost:" + str(master_addr) + "/notification/" + "put", data=notification_data))


# Client Handlers
@app.route('/exists/<path:file_location>', methods=['GET'])
def exists_handler(file_location):
    request_data = {"path": file_location}
    master_answer = request_master(request_data, "exists")
    return str(master_answer["exists"])


@app.route('/<path:file_location>', methods=['GET'])
def get_handler(file_location):
    request_data = {"path": file_location}
    master_answer = request_master(request_data, "get")
    response_data = {}
    global path_to_bytes
    if master_answer["gaddr"] == node_addr:
        response_data["bytes"] = path_to_bytes[file_location]
    else:
        response_data = request_node(master_answer["gaddr"], request_data, "get")
    return json.dumps(response_data)


@app.route('/<path:file_location>', methods=['PUT'])
def put_handler(file_location):
    request_data = request.json()
    request_data["path"] = file_location
    data = {"bytesLen": len(request_data["bytes"])}
    master_answer = request_master(data, "put")
    wlist = master_answer["wAddr"]
    response_data = {}
    if node_addr in wlist:
        wlist.remove(node_addr)
        global path_to_bytes
        path_to_bytes[file_location] = request_data[
            "bytes"]  # check if path already in path_to_bytes -> if so, response_data["success"] = False
        notification_data = {"path": file_location, "addr": node_addr}
        notify_master(notification_data)
        response_data["success"] = True
    for wAddr in wlist:
        request_data["path"] = file_location
        response_data["success"] = request_node(wAddr, request_data, "put")
        # if success == False -> throw exception
    return json.dumps(response_data)


@app.route('/copy', methods=['POST'])
def copy_handler():
    request_data = request.json()
    data1 = {"path": request_data["source_path"]}
    master_answer1 = request_master(data1, "get")
    global path_to_bytes
    if master_answer1["gaddr"] == node_addr:
        bytes_ = path_to_bytes[request_data["source_path"]]
    else:
        resp1 = request_node(master_answer1["gaddr"], request_data, "get")
        bytes_ = resp1["bytes"]
    data2 = {"bytesLen": len(bytes_)}
    master_answer = request_master(data2, "put")
    wlist = master_answer["wAddr"]
    response_data = {}
    if node_addr in wlist:
        wlist.remove(node_addr)
        path_to_bytes[request_data["destination_path"]] = request_data[
            "bytes"]  # check if path already in path_to_bytes -> if so, response_data["success"] = False
        notification_data = {"path": request_data["destination_path"], "addr": node_addr}
        notify_master(notification_data)
        response_data["success"] = True
    for wAddr in wlist:
        request_data["path"] = request_data["destination_path"]
        response_data["success"] = request_node(wAddr, request_data, "put")
        # if success == False -> throw exception
    return json.dumps(response_data)


# Node Communication  Handlers

@app.route('/node/<string:type_>', methods=['POST'])
def node_handler(type_):
    request_data = request.json()
    file_location = request_data["path"]
    response_data = {}
    global path_to_bytes

    if type_ == "get":
        response_data["bytes"] = path_to_bytes[request_data["path"]]
    elif type_ == "put":
        path_to_bytes[file_location] = request_data[
            "bytes"]  # check if path already in path_to_bytes -> if so, response_data["success"] = False
        notification_data = {"path": file_location, "addr": node_addr}
        notify_master(notification_data)
        response_data["success"] = True
    else:
        response_data["error"] = "unknownRequest"

    return json.dumps(response_data)


####################################################################################################

# ATTENTION : mettre des noms de route du style /mot1/mot2/mot3/... & pas de caractères spéciaux !!!
# Sinon spécifier params=my_data ds la route &&& ds la request !!!
@app.route('/heart', methods=['GET'])
def heartbeat():
    return json.dumps({"state": "alive"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('flask_port')
    args = parser.parse_args()
    port = int(args.flask_port)
    app.run(host="localhost", port=port)
