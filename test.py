import threading
import time


lock = threading.RLock()
def locks_and():
    with lock:
        time.sleep(2)
        print(time.time())
        return 0


def thread_function():
    locks_and()
    return

x = threading.Thread(target=thread_function)
x.start()
y= threading.Thread(target=thread_function)
y.start()
