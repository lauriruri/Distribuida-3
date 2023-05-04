#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 18:04:12 2023

@author: alumno
"""

from multiprocessing.connection import Listener
from multiprocessing import Process, Lock, Manager, Value, Condition, BoundedSemaphore
from multiprocessing.connection import AuthenticationError
import time
import timeit
import sys

#{N>=2}
N = 2 #numero de rondas = numero de jugadores (?) 

class Monitor():
    def __init__(self):
        self.mutex = Lock() #para el presentador
        self.candado = BoundedSemaphore(N-1) #para los jugadores
        self.npreguntasactuales = Value('i',0) # 0<= npreguntasactuales <= 1
        self.nrepuestasactuales = Value('i',0) # 0<= nrespuestasactuales <= N-1
        #self.manager = Manager()
        self.pregunta = ''
        self.respuesta = Manager().list()
        self.hacerpregunta = Condition(self.mutex)
        self.puedesresponder=Condition(self.mutex)
   
    #def si_pregunta(self) -> bool
    def si_preguntar(self)  ->bool :
        return self.npreguntasactuales.value == 0
   
    def si_responder(self) ->bool :
        return self.npreguntasactuales.value == 1 and \
               self.nrepuestasactuales.value >= 0 and \
               self.nrepuestasactuales.value < N
   
    def wants_preguntar(self):
        self.mutex.acquire()
        self.hacerpregunta.wait_for(self.si_preguntar)
        self.npreguntasactuales.value += 1
        self.mutex.release()

    def stop_pregununtar(self):
        self.mutex.acquire()
        self.npreguntasactuales.value -= 1
        self.mutex.release()

    def wants_responder(self):
        self.candado.acquire
        self.puedesresponder.wait_for(self.si_responder)
        self.nrepuestasactuales.value += 1
        self.candado.release
   
    def stop_responder(self):
        self.candado.acquire
        self.nrepuestasactuales.value -= 1
        self.candado.release


def jugadores(monitor:Monitor, conn, pid, npreguntas, nrespuestas, pregunta, respuesta_personal):
    #personas que juegan lo que propone el presentador
    contador = 0
   
    while contador != N: #numero de rondas de la partida
           #juega
           no_te_toca = "El juego empieza"
           conn.send(no_te_toca)
           nrespuestas.value += 1
           monitor.wants_responder()
           contador += 1
           print(contador)
           conn.send(pregunta)

           start = time.perf_counter()
           respuesta_personal = conn.recv
           end = time.perf_counter()
           time_para_responder = end - start
           monitor.stop_responder()


           #comprobar que si es la correcta
           #si muchos jugadores han respondido correctamente, gana el que ha respondido mas rapido
    conn.send("Game Over")
    conn.close()

           
def comprobar_tiempo(time_para_responder):
    pass


def presentador(monitor, conn, pid, npreguntas, nrespuestas, pregunta, respuesta):
    #persona que propone las preguntas/retos/pruebas
    contador = 0
    while contador != N : #NUMERO DE RONDAS
        monitor.wants_preguntar()
        te_toca = "Hacer una pregunta"
        conn.send(te_toca)
        pregunta = conn.recv()
        choices = "Dar 3 opciones, la primera debe ser la respuesta correcta"
        conn.send(choices)
        opciones = list(conn.recv())
        respuesta = opciones[0]
        contador += 1 #SUMO UNA RONDA

   
    conn.send("Game Over")
    conn.close()
       

def main(ip_address):
    monitor = Monitor()
    manager = Manager()
    npreguntas = manager.Value('i', 0) #controlar que solo haya 1
    nrespuestas = manager.Value('i', 0) #controlar cuantos jugadores HAN respondido
    nrondas = manager.Value('i',N)

    n_players = 0
    players = manager.list()
    pregunta = manager.list()
    respuestas_personales = [manager.Value('i', 0) for i in range(N)]  #????

    with  Listener(address=(ip_address, 6000),
                   authkey=b'secret password') as listener:
        print ('listener starting')
       
        while True:
            print ('accepting conexions')
            #CUANDO UNA PARTIDA COMIENZA OTROS JUGADORES PUEDEN EMPEZAR UNA NUEVA
            #ES ESTO UN PROBLEMA??? EL LISTENER SABE DIFERENCIAR LAS PARTIDAS??? NO ES UN PROBLEMA

            #TENEMOS QUE CREAR LOS PROCESOS CON DISTINTOS CANALES DE COMUNICACIÓN (VÉASE PINGPONG)
            try:
                conn = listener.accept()
                print ('connection accepted from', listener.last_accepted)
                players.append(listener.last_accepted) #cree la lista con los PID
               
                print('esto es n_players: ', n_players)
                n_players += 1 # cada vez que accepta un cliente, n_players se aumenta
                   
            except AuthenticationError:
                print ('Connection refused, incorrect password')
               
            if n_players == N:
               
                print(players)
               
                J = [Process(target=jugadores,
                            args=(monitor, conn,players[i], npreguntas,
                                  nrespuestas, pregunta, respuestas_personales[i].value)) for i in range(N - 1)  ]
                print('yeii')
               
                P = Process(target = presentador,
                            args = (monitor, conn, players[N-1], npreguntas,
                                    nrespuestas, pregunta, respuestas_personales))
                for k in J:
                    k.start()
                P.start()
                n_players = 0
           
           
           

           



if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)