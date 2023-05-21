# Distribuida- Práctica 3- Juego de preguntas

## Válidos archivos
Por ahora los archivos válidos son:
client_nuevasversiones.py, main_nuevasversiones.py : contienen el juego.

seleccionar.py, store_app.py : para poner el juego bonito están estos archivos hechos con la librería tkinter. Falta integrarlo en el otro código.

## Cómo funciona el juego
Los jugadores se connectan a la sala y se crea un proceso para cada uno. Cuándo hay el número de jugadores requirido, la sala cierra. Se distribuyen los papeles, uno es el que hace las preguntas y los otros responden.
El jugador que tiene el papel "question" propone una pregunta. Los otros esperan la pregunta y después responden. La pregunta se envía a un jugador: si este acierta, se lleva punto y se solicita otra pregunta al preguntador; si falla, esta pregunta 'rebota' y se enva a otro jugador.

Para poder jugar se tiene que ejecutar el archivo main_nuevasversiones.py (la sala) y, según está aquí el código, el archivo client_nuevasversiones.py en 3 terminales distintas (los jugadores: uno hace preguntas y los otros dos responden). Al final del archivo main_nuevasversiones.py en la línea 170, en 'main(ip_address, 3)', se puede cambiar el 3 al número de jugadores que se desee.

## Lista de Funciones en la clase QuizControl
- _ _init_ _ (self, manager, n_players, pointLimit): 
Inicializa los caracteristicos principales de un juego utilizando un manager para tener objectos compartidos. Se dedine los dos semaforos tipo Lock() que van a garantizar la exclusión mutua el los procesos según el papel de cada jugador.
- is_running(self):
Vuelve un booleano que indica si hay un juego.
- sum_point(self,n):
acumula un punto al jugador n
- lockQuestion(self), releaseQuestion(self):
hacen "acquire" y "release" al semaforo question correspondiente.
- lockNoQuestion(self), releaseNoQuestion(self):
hacen "acquire" y "release" al semaforo noquestion correspondiente.
- set_QA(self, question, answer):
reciben como argumentos la pregunta y la respuesta y las storan a la lista del manager self.QA.
- get_question(self):
devuelve el primer elemento de la lista QA, ie la pregunta
- answer_question(self, answer, n):
recibe como argumento la respuesta de cada jugador y comprueba si su respuesta está correcta. Si sí, devuelve True, y si no, False.
- str():
devuelve una cadena que se utiliza para la descripción del estado del juego



## Lista de Funciones auxiliares (archivo main)
- generateRoles(n):
recibe como argumento el número de los jugadores y distribuye los papeles a los jugadores.
- activateProcesses(processes)
recibe como argumento la lista de los procesos y los activa.

## Bloque de funciones auxiliares (archivo main)

generateRoles(n)
```python 
def generateRoles(n):
    roles = n * ["answer"]
    roles[randrange(n)] = "question"
    m = randrange(n)
    roles[m] = "question"
    return roles
```

activateProcesses(processes)
```python 
def activateProcesses(processes):
    for process in processes:
        process.start()
```

## Inclusiones - main
```python
from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Array, Semaphore
from random import randrange
import traceback
import sys
```
## Inclusiones - client
```python
from multiprocessing.connection import Client
import traceback
import sys
```

