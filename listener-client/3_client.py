from multiprocessing.connection import Client
import sys

def main(ip_address):
    print ('trying to connect')
    with Client(address=(ip_address, 6000), authkey=b'secret password') as conn:
        print ('connection accepted')
        answer = ''
        while answer != 'adios':
            message = input('Message to send? ')
            print ('sending message')
            conn.send(message)
            answer = conn.recv()
            print ('received message', answer)


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
