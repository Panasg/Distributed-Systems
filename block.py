from time import time
from flask import Flask, jsonify, request
import requests
import json
import threading

import data
import utilities

class block:

    def __init__(self,index, timestamp, transactions,nonce, current_hash=None, previous_hash=None):
        self.index=index
        self.timestamp=timestamp
        self.transactions=transactions

        self.nonce=nonce
        self.current_hash=current_hash
        self.previous_hash=previous_hash


    def hash(self):
        transactionsAsList=[]
        for trans in self.transactions:
            transactionsAsList.append(trans.asDictionary())

        tempDict={
            "index":self.index,
            "transactions":transactionsAsList,
            "previous_hash":self.previous_hash,
            "nonce":self.nonce
        }

        asString=json.dumps(tempDict,sort_keys=True)
        hash = utilities.hashStringToString(asString)
        return hash

    def asDictionary(self):
        transactionsAsList=[]
        for trans in self.transactions:
            transactionsAsList.append(trans.asDictionary())
        tempDict={
            "index":self.index,
            "timestamp":self.timestamp,
            "transactions":transactionsAsList,
            "nonce":self.nonce,
            "current_hash":self.current_hash,
            "previous_hash":self.previous_hash,
        }
        return tempDict

'''
def new_block(self, proof, previous_hash,transactions):
    block = {
        'index': len(self.chain) + 1,
        'timestamp': time(),
        'transactions': transactions,
        'proof': proof,
        'previous_hash': previous_hash or self.hash(self.chain[-1]),
        'current_hash':"string"
    }
    block['current_hash']=self.hash(block)

    # Reset the current list of transactions
    if(len(self.chain)==0 and data.myPort==data.adminPort):
        self.chain.append(block)
        return block


    response=requests.get("http://localhost:"+str(data.myPort)+"/nodes/resolve")
    #self.current_transactions = []
    if(response.status_code==200):
        self.chain.append(block)#mpainei sthn lista mas
        broadcast.broadcast_a_block(block,self)
    return block
'''

def createGenesisBlock(transactions):#mono o admin to ektelei

    timestamp=time()
    genBlock=block(0,time(),transactions,0,"1",1)
    genBlock.current_hash= genBlock.hash()

    return genBlock
