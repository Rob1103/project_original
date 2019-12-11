__version__ = "1.0"

import argparse
import flask
import hashlib
import numpy
import requests
import time

from threading import Thread

from dftfs.master import *
from dftfs.node import *

parser = argparse.ArgumentParser()
parser.add_argument('arg')
args = parser.parse_args()
nb_nodes = int(args.arg)

assert (0 < nb_nodes < 11)  # 11 threads max for a local computer

thread0 = Master(nb_nodes, "localhost", 1024)  # IP + port of master
thread0.start()
for i in range(nb_nodes):
    # IP + port of master and IP + port of node. Master knows node at 1st heartbeat
    thread1 = Node("localhost", 1024, "localhost", 2000 + i)
    thread1.start()
thread0.join()
