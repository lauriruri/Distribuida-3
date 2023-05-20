from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Array, Semaphore
from random import randrange
import traceback
import sys

class QuizControl():
    def __init__(self, manager, n_players, pointLimit):
        self.numberP    = n_players
        #                               Q   A
        self.QA         = manager.list(["", ""])
        self.Points     = manager.list([0] * n_players)
        self.limit      = pointLimit
        self.running    = manager.Value('i', 1)
        self.question   = manager.Lock()
        self.noquestion = manager.Lock()
        self.question.acquire()
        
    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.running.value = 0

    def sum_point(self, n):
        self.Points[n] += 1

    def printSemaphore(self):
        print(self.question)
        
    def lockQuestion(self):
        self.question.acquire()

    def releaseQuestion(self):
        self.question.release()

    def lockNoQuestion(self):
        self.noquestion.acquire()

    def releaseNoQuestion(self):
        self.noquestion.release()
        
    def set_QA(self, question, answer):
        self.QA[0] = question
        self.QA[1] = answer
        
    def get_question(self):
        return self.QA[0]
    
    def answer_question(self, answer, n):
        if self.QA[1] == answer:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.QA} | {self.Points} | running: {self.running.value} | {self.question} | {self.noquestion}"

def player(conn, pid, role, n, rounds, QC):
    try:
        conn.send(role)        
        if role != "question":
            username = conn.recv()

        while QC.is_running() and rounds != 0:
            if role == "question":
                QC.lockNoQuestion()
                conn.send("QA!")
                question, answer = conn.recv()
                QC.set_QA(question, answer)
                QC.releaseQuestion()
                
            else: #la partida no acaba hasta que todos los jugadores hayan obtenido rounds puntos
                QC.lockQuestion()
                #sem.acquire()
                conn.send(QC.get_question())
                answer = conn.recv()
                if QC.answer_question(answer, n):
                    conn.send("right!")
                    rounds = rounds - 1
                    QC.releaseNoQuestion()
                else:
                    conn.send("wrong!")
                    QC.releaseQuestion()
                #sem.release()
        if role != "question" and rounds == 0:
            conn.send("Se acabó la partida! Terminaste en el puesto ") #ver cómo enviar el puesto
                    
    except EOFError:
        print(f"[Server]: Client {pid} disconnected abruptly.")
        running = False

    except Exception as e:
        print(f"Something went wrong | {pid}, {role}, {n}, {QC}")
        print(e)
        running = False
            
    conn.close()
    

def main(ip_address, n_t_players):
    running  = True
    listener = Listener(address=(ip_address, 6000)
                        , authkey=b'secret')
    print("      Listener started")
    print("------------------------------")
    
    rounds = 3
    n_players = 0
    players   = [None] * n_t_players
    roles = generateRoles(n_t_players)
    manager   = Manager()
    QA = QuizControl(manager, n_t_players, 3)

    while running:
        try:
            conn         = listener.accept()
            address, pid = listener.last_accepted
            print(f"[Server]: { pid } Connected!")
            
            players[n_players] = Process(target=player
                                         ,args = (conn
                                                  , pid
                                                  , roles[n_players]
                                                  , n_players
                                                  , rounds
                                                  , QA))
            n_players += 1
            print(f"number of players: {n_players}")
            
            if n_players == n_t_players:
                print("Starting game")
                activateProcesses(players)
                n_players = 0
                players   = [None] * n_t_players

        except Exception as e:
            traceback.print_exc()
            print(e)

    print("Server closed")

# ------------------------------
#       Helper functions
# ------------------------------
def activateProcesses(processes):
    for process in processes:
        process.start()

def generateRoles(n):
    roles = n * ["answer"]
    m = randrange(n)
    roles[m] = "question"
    return roles

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
    main(ip_address, 3)
