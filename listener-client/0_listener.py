from multiprocessing.connection import Listener
import sys

def main(ip_address):
    listener = Listener(address=(ip_address, 6000),
                        authkey=b'secret password')
    print ('listener starting')
    conn = listener.accept()
    print ('connection accepted from', listener.last_accepted)
    m = conn.recv()
    print ('received message:', m)
    conn.send('ok')
    conn.close()
    print ('connection closed')
    listener.close()


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
