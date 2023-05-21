from multiprocessing.connection import Client
import traceback
import sys

def client(ip_address):
    running = True
    try:
        client   = Client(address=(ip_address, 6000), authkey=b'secret')
        role = client.recv()
        
        if role != "question":
            username = input("username: ")            
            client.send(username)

        while running:
            if role == "question":
                message = client.recv()
                print(f"the message is: {message}")
                if "gracias" in message:
                    print(message)
                    client.close()
                    running = False

                else:
                    question = input("Question to be asked: ")
                    answer   = input("Valid answer: ")
                    print("------------------------------")
                    client.send([question, answer])
            
            else:
                message = client.recv()
                if "termino" in message:
                    print(message)
                    client.close()
                    running = False

                else:
                    print(message)
                    answer = input("Answer to the question: ")
                    client.send(answer)
                    result = client.recv()
                    print(result)

    except Exception as e:
        traceback.print_exc()
        print(e)
        print(type(e))

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]

    client(ip_address)

        
