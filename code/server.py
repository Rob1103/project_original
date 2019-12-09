import argparse
import flask
import hashlib
import numpy
import requests
import time

from threading import Thread

from dftfs.master import *

parser = argparse.ArgumentParser()
parser.add_argument('arg')
args = parser.parse_args()
nb_nodes = int(args.arg)

assert (0 < nb_nodes < 21)

thread0 = Master(nb_nodes)
thread0.start()
thread0.join()
