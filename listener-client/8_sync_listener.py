from multiprocessing.connection import Listener
import time
import random
listener = Listener(address=('127.0.0.1', 6000), authkey=b'secret password')
print ('listener starting')
conn = listener.accept()
print ('connection accepted from', listener.last_accepted)
time.sleep(random.random()*3)
for i in range(10):
    m = conn.recv()
    print ('received message:', m)
    conn.send('ok')
    time.sleep(random.random()*3)
conn.close()
print ('connection closed')
listener.close()
