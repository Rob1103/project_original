# app / __init__.py

import argparse
from flask import Flask
import hashlib
import numpy
import requests
import time

from threading import Thread

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello world !"


class Master(Thread):
    def __init__(self, nb_nodes, ip, port):
        Thread.__init__(self)
        self.nb_nodes = nb_nodes
        self.ip = ip
        self.port = port
        self.addr = "http://" + ip + ":" + str(port)

        self.nodes_ls = [((None, 2000), "dead")] * nb_nodes
        for node in range(nb_nodes):
            self.nodes_ls[node] = ((None, 2000 + node), "dead")
        self.files = []

    def run(self):
        app.run(host=self.ip, port=self.port)
