import data
from flask import Flask, jsonify, request
import requests
import json
import threading
import time

def broadcast_a_transaction(blockchain,body):
    kwargs = {}
    kwargs['timeout'] = 25
    print(f"Nodes {blockchain.nodes}")
    for node in blockchain.nodes:
        '''
        if ("localhost:"+str(data.myPort)) == node:
            blockchain.validate_transaction(body)
            indexOfBlock = blockchain.new_transaction(body['sender'], body['recipient'], body['amount'],body['index'])
            print(f"Current Transactions {blockchain.current_transactions}")

        else:
        '''
        print(node+"/receiveATransaction")
        response=requests.post("http://"+node+"/receiveATransaction",json=body,**kwargs)
        print(response.status_code)

def broadcast_a_block(block,blockchain):
    kwargs = {}
    kwargs['timeout'] = 25
    for node in blockchain.nodes:
        response=requests.post("http://"+node+"/receiveABlock",json=block,**kwargs)
        print(response.status_code)
