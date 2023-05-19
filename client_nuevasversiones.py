from multiprocessing.connection import Client
import traceback
import sys

def client(ip_address):
    try:
        client   = Client(address=(ip_address, 6000), authkey=b'secret')
        
        role = client.recv()
        
        if role != "question":
            username = input("username: ")            
            client.send(username)

        while True:
            if role == "question":
                question = input("Question to be asked: ")
                answer   = input("Valid answer: ")
                print("------------------------------")
                client.send([question, answer])
            
            else:
                question = client.recv()
                print(question)
                answer = input("Answer to the question: ")
                client.send(answer)
                result = client.recv()
                print(result)

        client.close()

    except Exception as e:
        print(e)
        print(type(e))

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]

    client(ip_address)

        
        


    

