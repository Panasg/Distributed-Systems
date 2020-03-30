import data
import threading
import broadcast
import time
import utilities
from random import seed,randint


def mine():
    x = threading.Thread(target=mine_thread)
    with data.miningLock:
        if not data.someoneIsMining:
            data.someoneIsMining=True
            x.start()
        else:
            print("Mining is already taking place")            
    return

def mine_thread():
    seed()
    with data.lock:
        listOfTrans=[]
        for trans in data.current_transactions.values():
            listOfTrans.append(trans.asDictionary())

        dictionary={
            'index':data.blockchain.chain[-1].index+1,
            'timestamp':time.time(),
            'transactions':listOfTrans,
            'nonce': (randint(0, 100000)),
            'current_hash':'1234',
            'previous_hash':data.blockchain.chain[-1].current_hash
        }
    testingBlock=utilities.asObject(dictionary,"block")

    magicNonce=proof_of_work(testingBlock)
    testingBlock.current_hash=testingBlock.hash()#εχουμε το σωστο hash πλεον

    print(f"I mined this block {testingBlock.current_hash} {testingBlock.nonce}")
    broadcast.broadcast_a_block(testingBlock)

    with data.miningLock:
        data.someoneIsMining=False

    return

def proof_of_work(block):#βρισκει το καταλληλο nonce και το αποθηκευει
    while valid_proof(block) is False:
        block.nonce += 1
    return block.nonce


def valid_proof(block):
    guess_hash = block.hash()
    return guess_hash[:data.difficulty] == '0'*data.difficulty
