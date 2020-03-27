from time import time
from flask import Flask, jsonify, request
import requests
import json
import threading

import data
import utilities

class transaction:

    def __init__(self,sender, recipient, amount,timestamp, inputs,outputs, id=None, signature=None):
        self.sender=sender
        self.recipient=recipient
        self.amount=amount
        self.timestamp=timestamp

        self.inputs=inputs
        self.outputs=outputs
        self.id=id
        self.signature=signature

    def calculateId(self):
        tempDict={
            "sender":self.sender,
            "recipient":self.recipient,
            "timestamp":self.timestamp
        }

        asString=json.dumps(tempDict,sort_keys=True)
        hash = utilities.hashStringToString(asString)
        return hash

    def asDictionary(self):
        tempDict={
            "sender":self.sender,
            "recipient":self.recipient,
            "amount":self.amount,
            "timestamp":self.timestamp,
            "inputs":self.inputs,
            "outputs":self.outputs,
            "id":self.id,
            "signature":self.signature

        }
        return tempDict




def createGenesisTransaction():#mono o admin to ektelei

    timestamp=time()
    genTransaction=transaction(0,data.publicKey,100*data.numOfParticipants,timestamp,[],[])
    genTransaction.id= genTransaction.calculateId()

    return genTransaction
