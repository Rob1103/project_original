# app / __init__.py

import argparse
from flask import Flask, json, jsonify
import hashlib
import numpy
import requests
from requests.exceptions import Timeout
import time

from threading import Thread

# global variables should always be declared "global" before being used in functions (see index())
port = 0
master_addr = 1024

node_addr
path_to_bytes

app = Flask(__name__)

###################################################################################################

def requestMaster(requestData, type):
    return json.dumps(requests.post(url = "http://localhost:" + master_addr + "/request/" + type, data = requestData))

def requestNode(gAddr, requestData, type):
    return json.dumps(request.post(url = "http://localhost:" + gAddr + "/node/" + type, data = requestData))

def notifyMaster(notificationData):
    return json.dumps(request.post(url = "http://localhost:" + master_addr + "/notification/" + "put", data = notificationData))

# Client Handlers
@app.route('/exists/<path:fileLocation>', methods=['GET'])
def exist_handler(fileLocation):
    requestData = {}
    requestData["path"] = fileLocation
    masterAnswer = requestMaster(requestData, "exist")
    return json.dumps(masterAnswer)

@app.route('/<path:fileLocation>', methods=['GET'])
def get_handler(fileLocation)
    requestData = {}
    requestData["path"] = fileLocation
    masterAnswer = requestMaster(requestData, "get")
    if masterAnswer["gAddr"] == node_addr:
        responseData["bytes"] = global path_to_bytes[fileLocation]
    else:
        responseData = requestNode(masterAnswer["gAddr"], requestData, "get")
    return json.dumps(responseData)

@app.route('/<path:fileLocation>', methods=['PUT'])
def put_handler(fileLocation):
    requestData = request.json()
    requestData["path"] = fileLocation
    data = {}
    data["bytesLen"] = len(requestData["bytes"])
    masterAnswer = requestMaster(data, "put")
    wList = masterAnswer["wAddr"]
    responseData = {}
    if node_addr in wList:
        wList.remove(node_addr)
        global path_to_bytes[fileLocation] = requestData["bytes"] #check if path already in path_to_bytes -> if so, responseData["success"] = False
        notificationData = {}
        notificationData["path"] = fileLocation
        notificationData["addr"] = node_addr
        notifyMaster(notificationData)
        responseData["success"] = True
    for wAddr in wList:
        responseData["success"] = requestNode(wAddr, requestData, "put")
        # if success == False -> throw exception
    return json.dumps(responseData)
    
@app.route('/copy', methods=['POST'])
def copy_handler():
    requestData = request.json()
    responseData = {}
    data1 = {}
    data1["path"] = requestData["source_path"]
    masterAnswer1 = requestMaster(data1, "get")
    if masterAnswer1["gAddr"] == node_addr:
        bytes = global path_to_bytes[requestData["source_path"]]
    else:
        resp1 = requestNode(masterAnswer["gAddr"], requestData, "get")
        bytes = resp1["bytes"]
    data2 = {}
    data2["bytesLen"] = len(bytes)
    masterAnswer = requestMaster(data2, "put")
    wList = masterAnswer["wAddr"]
    responseData = {}
    if node_addr in wList:
        wList.remove(node_addr)
        global path_to_bytes[fileLocation] = requestData["bytes"] #check if path already in path_to_bytes -> if so, responseData["success"] = False
        notificationData = {}
        notificationData["path"] = fileLocation
        notificationData["addr"] = node_addr
        notifyMaster(notificationData)
        responseData["success"] = True
    for wAddr in wList:
        responseData["success"] = requestNode(wAddr, requestData, "put")
        # if success == False -> throw exception
    return json.dumps(responseData)
    
# Node Communication  Handlers

@app.route('/node/<string:type>', methods=['POST'])
def node_handler(type):
    requestData = request.json()
    responseData = {}
    
    if (type == "get"):
        responseData["bytes"] = global path_to_bytes[requestData["path"]]
    elif (type == "put"):
        global path_to_bytes[fileLocation] = requestData["bytes"] #check if path already in path_to_bytes -> if so, responseData["success"] = False
        notificationData = {}
        notificationData["path"] = fileLocation
        notificationData["addr"] = node_addr
        notifyMaster(notificationData)
        responseData["success"] = True
    else:
        responseData["error"] = "unknownRequest"

    return json.dumps(responseData)

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
