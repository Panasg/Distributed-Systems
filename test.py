import threading
import time
import block


bl=block.createGenesisBlock([])

str=bl.hash()
by=bl.hash().encode()
#print(bl.hash().hexdigest())
print(bytes(str,'utf-8'))
print(by)
for byte in by:
    print(byte)
