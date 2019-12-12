# app / __init__.py

import argparse
from flask import Flask
import hashlib
import numpy
import requests
import time

from threading import Thread

# global variables should always be declared "global" before being used in functions (see index())
nb_nodes = 0
ip_ = 0
port_ = 0
nodes_ls = []
files = []

app = Flask(__name__)


@app.route('/')
def index():
    global nb_nodes
    print(nb_nodes)
    return "Hello world !"


@app.route('/heartbeat/<ip>/<port>')
def heartbeat(ip, port):
    return "Hello world !"  # implement heartbeat


class Master(Thread):
    def __init__(self, nbnodes, ip, port):
        Thread.__init__(self)
        global nb_nodes
        nb_nodes = nbnodes
        global ip_
        ip_ = ip
        global port_
        port_ = port

        global nodes_ls
        nodes_ls = [((None, 2000), "dead")] * nb_nodes
        for node in range(nb_nodes):
            nodes_ls[node] = ((None, 2000 + node), "dead")
        global files
        files = []

    def run(self):
        global ip_
        global port_
        app.run(host=ip_, port=port_)
