# app / __init__.py

import argparse
from flask import Flask
import hashlib
import numpy
import requests
import time

from threading import Thread

# global variables should always be declared "global" before being used in functions (see index())
port = 0
nb_nodes = 0
nodes_ls = []
files_locations = []

app = Flask(__name__)


@app.route('/')
def index():
    global nb_nodes
    print(nb_nodes)
    return "Hello world !"


@app.route('/heartbeat/<ip>/<port>')
def heartbeat(ip, port):
    return "Hello world !"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('nodes')
    parser.add_argument('flask_port')
    args = parser.parse_args()
    nb_nodes = int(args.nodes)
    port = int(args.flask_port)
    nodes_ls = [((None, 2000), "dead")] * nb_nodes
    for node in range(nb_nodes):
        nodes_ls[node] = ((None, 2000 + node), "dead")
    app.run(host="localhost", port=port)
    new watchdog
    waitforhearbeat()

class Watchdog:
    

