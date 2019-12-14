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
master_port = 0
files = []

app = Flask(__name__)


@app.route('/')
def index():
    return "Ok"


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
