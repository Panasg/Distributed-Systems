import threading
import time
import block
import mining

bl=block.createGenesisBlock([])

print(time.time())
mining.proof_of_work(bl)
bl.current_hash=bl.hash()
print(time.time())
print(bl.asDictionary())
