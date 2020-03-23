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
        print(node+"/receiveATransaction")
        response=requests.post("http://"+node+"/receiveATransaction",json=body,**kwargs)
        print(response.status_code)
