from multiprocessing.connection import Client
import sys

def main(ip_address):
    print ('trying to connect')
    with Client(address=(ip_address, 6000), authkey=b'secret password') as conn:
        print ('connection accepted')
        cont = True
       
           
        while cont:
           
            if conn.recv == "El juego empieza" : #eres jugador
                respuesta = input("Dar respuesta") #quizas aqui podemos poner un "timer"
                conn.send(respuesta)
               
            elif conn.recv == "Hacer una pregunta" : #eres el presentador

                message = input('Pregunta para enviar?) ')
                print ('sending message')
                conn.send(message)
                choices = input("Dar opciones")
                conn.send(choices)



if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)