from multiprocessing.connection import Listener
from multiprocessing import Process, Lock, Manager, Value, Condition, current_process
from multiprocessing.connection import AuthenticationError
from time import time
import sys


N = 2 #numero de rondas = numero de jugadores (?)

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.npreguntasactuales = Value('i',0) # 0<= npreguntasactuales <= 1
        self.nrepuestasactuales = Value('i',0) # 0<= nrespuestasactuales <= N-1
        #self.manager = Manager()
        self.pregunta = ''
        self.respuesta = Manager().list()
        self.haypregunta = Condition(self.mutex)
    
    #def si_pregunta(self) -> bool

    def wants_preguntar(self):
        self.mutex.acquire()
        self.npreguntando.value += 1



conn,listener.last_accepted, npreguntas, njugadores, nrondas
listener.accept() = conn

def jugadores(monitor:Monitor, njugadores:Value, npreguntas:Value , nrondas:Value):
    #personas que juegan lo que propone el presentador
    contador = 0
    while contador != nrondas: #numero de rondas de la partida
           #juega
           njugadores += 1
           monitor.wants_jugar()
           contador += 1

def presentador(monitor:Monitor, njugadores:Value, npreguntas:Value , nrondas:Value):
    #persona que propone las preguntas/retos/pruebas
    contador = 0
    while contador != nrondas: 
        contador += 1

'''
def serve_client(conn, pid, candado, npreguntas, njugadores, nrondas, players):
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
'''


def main(ip_address):
    npreguntas = Manager().Value('i', 0) #controlar que solo haya 1
    nrespuestas = Manager().Value('i', 0) #controlar cuantos jugadores HAN respondido
    nrondas = Manager().Value('i',N)

    n_players = 0
    players = Manager().list()

    with  Listener(address=(ip_address, 6000),
                   authkey=b'secret password') as listener:
        print ('listener starting')

        while n_players != N-1 : #numero de jugadores que quiero
            print ('accepting conexions')

            try:
                conn = listener.accept()
                print ('connection accepted from', listener.last_accepted)
                p = Process(target=jugadores, name = listener.last_accepted, args=(conn,listener.last_accepted,candado, npreguntas, nrespuestas, nrondas))
                players.append(p)
                n_players += 1

            except AuthenticationError:
                print ('Connection refused, incorrect password')
        
        conn = listener.accept()
        print ('connection accepted from', listener.last_accepted)
        p = Process(target = presentador , name = listener.last_accepted, args=(conn,listener.last_accepted,candado, npreguntas, nrespuestas, nrondas))
        players.append(p)
        n_players += 1

        for i in range(0,len(players)):
            players[i].start()
            players[i].join()

        print ('end')

if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)