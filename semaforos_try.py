from multiprocessing.connection import Listener
from multiprocessing import Process, Lock, Manager, Value, Condition, current_process
from multiprocessing.connection import AuthenticationError
from time import time
import sys

candado = Lock()
candado.acquire()

def main():
    try:
        candado.acquire(timeout=2)
        print('hola')
    except:
        print('adios')