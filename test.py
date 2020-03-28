import threading
import time

def sleepF():
    time.sleep(3)
    return

def start_a_thread():
    x = threading.Thread(target=sleepF)
    x.start()
    return "ok"

    print("done")
    x.join()


for i in range (0,2):
    x=input()
    start_a_thread()
