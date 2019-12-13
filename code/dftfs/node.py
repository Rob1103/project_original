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
master_ip = "localhost"
master_port = 0
files = []

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello world !"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('flask_port')
    args = parser.parse_args()
    port = int(args.flask_port)
    app.run(host="localhost", port=port)
