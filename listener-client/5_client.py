from multiprocessing.connection import Client
import sys

def main(ip_address):
    print ('trying to connect')
    with Client(address=(ip_address, 6000), authkey=b'secret password') as conn:
        print ('connection accepted')
        cont = True
        while cont:
            message = input('Message to send? n -> send but no wait for answer) ')
            print ('sending message')
            conn.send(message)
            if message=='n':
                cont = False
            else:
                answer = conn.recv()
                print ('received message', answer)
                cont = answer!='adios'


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
