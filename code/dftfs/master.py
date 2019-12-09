import argparse
import flask
import hashlib
import numpy
import requests
import time

from threading import Thread

import random
import sys

class Master(Thread):
    def __init__(self, lettre):
        Thread.__init__(self)
        self.lettre = str(lettre)

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        i = 0
        while i < 20:
            sys.stdout.write(self.lettre)
            sys.stdout.flush()
            attente = 0.2
            attente += random.randint(1, 60) / 100
            time.sleep(attente)
            i += 1
            print(i)
