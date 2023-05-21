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
        self.limit      = pointLimit
        self.points     = manager.dict()
        self.question   = manager.Lock()
        self.noquestion = manager.Lock()
        self.question.acquire()

    def sum_point(self, username):
        self.points[username] += 1

    def add_user_to_points(self, username):
        self.points[username] = 0
        
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
        return f"{self.QA} | {self.points} | {self.question} | {self.noquestion}"

def player(conn, pid, role, n, max_points, QC, n_t_players):
    try:
        conn.send(role)        
        if role != "question":
            username = conn.recv()
            QC.add_user_to_points(username)

        while max_points not in QC.points.values():
            if role == "question":
                QC.lockNoQuestion()
                
                if max_points in QC.points.values():
                    QC.releaseNoQuestion()
                    QC.releaseQuestion()
                    break

                conn.send("QA!")
                question, answer = conn.recv()
                QC.set_QA(question, answer)
                QC.releaseQuestion()
                
            else:
                QC.lockQuestion()
                
                if max_points in QC.points.values():
                    QC.releaseQuestion()
                    break

                conn.send(QC.get_question())
                answer = conn.recv()
                
                if QC.answer_question(answer, n):
                    QC.sum_point(username)
                    conn.send("right!")
                    QC.releaseNoQuestion()
                else:
                    conn.send("wrong!")
                    QC.releaseQuestion()

        if role != "question":
            conn.send(f"termino {QC.points}")
            conn.close()

        elif role == "question":
            conn.send("Muchas gracias por jugar :)")
            conn.close()
                    
    except EOFError:
        print(f"[Server]: Client {pid} disconnected abruptly.")
        running = False

    except Exception as e:
        print(f"Something went wrong | {pid}, {role}, {n}")
        print(QC)
        print(f"error: {e}")
        print(type(e))
        running = False
    
def main(ip_address, n_t_players):
    running  = True
    listener = Listener(address=(ip_address, 6000)
                        , authkey=b'secret')
    print("      Listener started")
    print("------------------------------")
    
    maxPoints = 3
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
                                                  , maxPoints
                                                  , QA
                                                  ,n_t_players))
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
    #aqui ponemos el numero de jugadores que queremos que haya
