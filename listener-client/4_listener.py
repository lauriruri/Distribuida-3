from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError
import sys

def accept_connection(listener):
    try:
        with listener.accept() as conn:
            print ('connection accepted from', listener.last_accepted)
            open_conn = True
            while open_conn:
                m = conn.recv()
                print ('received message:', m)
                if m == 'hola':
                    answer = 'adios'
                    open_conn = False
                else:
                    answer = 'ok'
                conn.send(answer)
        print ('connection closed')
    except AuthenticationError:
        print ('Connection refused, incorrect password')


def main(ip_address):
    with Listener(address=(ip_address, 6000),
                  authkey=b'secret password') as listener:
        print ('listener starting')
        while True:
            accept_connection(listener)


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
