from multiprocessing.connection import Client

import sys
def main(ip_address):
    print (f'trying to connect {ip_address}')
    conn = Client(address=(ip_address, 6000), authkey=b'secret password')
    print ('connection accepted')

    print ('sending message')
    conn.send('hello world')
    print ('received message', conn.recv())
    conn.close()


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
