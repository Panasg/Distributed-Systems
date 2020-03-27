import utilities

import time

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


dicti={
    "name":'kalhmera',
    "amout":2,
    "timestamp":current_time
}


print(utilities.hashStringToString(str(dicti)))
