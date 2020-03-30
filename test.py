import threading
import time
import block
import mining

from random import seed,randint

seed()

bl=block.createGenesisBlock([])


print(randint(1,100000))

print(time.time())
mining.proof_of_work(bl)
bl.current_hash=bl.hash()
print(time.time())
print(bl.asDictionary())
