# app / __init__.py

import argparse
from flask import Flask
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

app = Flask(__name__)


class Watchdog(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global nodes_ls
        while True:
            time.sleep(3)
            for n in nodes_ls:
                data = {}
                try:
                    response = requests.get("http://localhost:" + str(n[0]) + "/heart", timeout=2)
                except Timeout:
                    lst = list(n)
                    lst[1] = "dead"
                    n = tuple(lst)
                    duplicate_data()  # duplicate
                    continue
                try:
                    data = response.json()
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
