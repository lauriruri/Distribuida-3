from multiprocessing.connection import Client
import time
import random

print ('trying to connect')
conn = Client(address=('127.0.0.1', 6000), authkey=b'secret password')
print ('connection accepted')
for i in range(10):
    time.sleep(random.random()*3)
    msg = f"msg{i}"
    print(f"sending {msg}")
    conn.send(msg)
    conn.recv()
conn.close()
