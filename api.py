import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
import threading

import block_chain
import data
import wallet
import setupNetwork

# Instantiate the Node
app = Flask(__name__)

@app.route('/receive_transaction', methods=['POST'])
def receive_transaction():
    return

@app.route('/receiveABlock', methods=['POST'])
def receive_a_block():
    values = request.get_json()
    required = ['index', 'transactions', 'timestamp','proof','previous_hash','current_hash']
    if not all(k in values for k in required):
        return 'Missing values', 400
    my_block = blockchain.imported_block(values['index'], values['transactions'], values['timestamp'],values['proof'],values['previous_hash'],values['current_hash'])
    print(f"Current Blocks {data.blockchain.chain}")
    response = {'message': f'Block will be added {my_block}'}
    return str(response), 200

@app.route('/new_transaction', methods=['POST'])
def create_transaction():
    return

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': data.blockchain.chain,
        'length': len(data.blockchain.chain),
    }
    return str(response), 200

@app.route('/show_balance',methods=['GET'])
def show_balance():
    return

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    print("I am getting register request")
    values = request.get_json()

    setupNetwork.saveNodes(values)
    return "ok",200



@app.route('/view_transactions', methods=['GET'])
def view_transactions():
    return

@app.route('/setup', methods=['GET'])
def setup():

    if data.myPort!=data.adminPort:
        res={"Message":"I Ain't admin"}
        return jsonify(res),200
    else:
        values=request.get_json()
        res={"Message":"Wait for everybody to start"}
        setupNetwork.register(values)

    return "OK",200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-a', '--admin', default=5000, type=int, help='port of admin')
    args = parser.parse_args()

    data.myPort=port = args.port
    data.adminPort=args.admin
    data.myUrl=f"http://localhost:{data.myPort}"
    wallet.initKeys()

    data.blockchain = block_chain.Blockchain()

    print(f'My port {data.myPort} ,Admin\'s port {data.adminPort}')
    print(f'My publicKey {data.publicKey}')


    myInfo={
        "url":f"http://localhost:{data.myPort}",
        "publicKey":data.publicKey
    }
    if data.myPort!=data.adminPort:#expecting admin to be listening
        kwargs = {}
        kwargs['timeout'] = 5
        setupResponse=requests.get(f'http://localhost:{data.adminPort}/setup',json=myInfo,**kwargs)
        #print(f"Setup Response {setupResponse}")
    else:#admin is not listening yet
        setupNetwork.register(myInfo)



    app.run(host='0.0.0.0', port=port)
    print("After run")
