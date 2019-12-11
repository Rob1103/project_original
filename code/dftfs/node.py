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


class Node(Thread):
    def __init__(self, master_ip, master_port, ip, port):
        Thread.__init__(self)
        self.master_ip = master_ip
        self.master_port = master_port
        self.ip = ip
        self.port = port
        self.master_addr = "http://" + master_ip + ":" + str(master_port)
        self.addr = "http://" + ip + ":" + str(port)

        self.files = []

    def run(self):
        app.run(host=self.ip, port=self.port)
