from multiprocessing.connection import Listener
from multiprocessing import Process
from multiprocessing.connection import AuthenticationError
from time import time
import sys

def serve_client(conn, pid):
    while True:
        try:
            m = conn.recv()
        except EOFError:
            print ('No receive, connection abruptly closed by client')
            break
        print (f'received message: {m} from {pid}')
        answer = 'ok'
        conn.send(answer)
    conn.close()
    print (f'connection {pid} closed')

def main(ip_address):
    with  Listener(address=(ip_address, 6000),
                   authkey=b'secret password') as listener:
        print ('listener starting')

        while True:
            print ('accepting conexions')
            try:
                conn = listener.accept()
                print ('connection accepted from', listener.last_accepted)
                p = Process(target=serve_client, args=(conn,listener.last_accepted))
                p.start()
            except AuthenticationError:
                print ('Connection refused, incorrect password')
        print ('end')

if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
