import threading
import time
import block
import mining
import data

from random import seed,randint
'''
seed()

bl=block.createGenesisBlock([])

for i in range (1,6):
    data.difficulty=i
    print(f"\nDificculty {i}")
    t1=time.time()
    mining.proof_of_work(bl)
    bl.current_hash=bl.hash()
    print(f"Time {time.time()-t1}")
    print(f"{bl.current_hash} {bl.nonce}")
#print(bl.asDictionary())
'''
first = [1,2]
sec=first[:]
first.append(3)
print(first)
print(sec)
