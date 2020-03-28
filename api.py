import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
import threading
import broadcast
import transaction
import block_chain
import data
import wallet
import setupNetwork
import utilities
# Instantiate the Node
app = Flask(__name__)

@app.route('/receive_transaction', methods=['POST'])
def receive_transaction():

    values=request.get_json()
    required = ['sender', 'recipient', 'amount','timestamp', 'inputs','outputs', 'id', 'signature']
    if not all(k in values for k in required):

        return 'Missing values', 400

    trans_obj=utilities.asObject(values,"transaction")
    #print("BEFORE SIGNATURE")
    trans_obj.verify_signature()
    retValue=trans_obj.validate_transaction()
    if(retValue):
        with data.lock:
            data.current_transactions.append(trans_obj)
    #print("AFTER SIGNATURE")
    return "transaction recieved",200
    #trans_obj.validate()
@app.route('/receiveABlock', methods=['POST'])
def receive_a_block():
    values = request.get_json()
    required = ['index', 'transactions', 'timestamp','nonce','previous_hash','current_hash']
    if not all(k in values for k in required):
        return 'Missing values', 400

    my_block=utilities.asObject(values,'block')

    with data.lock:
        for transaction in my_block.transactions:
            transaction.validate_transaction()
        data.blockchain.chain.append(my_block)
    print(data.utxos)
    print(f"Current Blocks :")
    data.blockchain.print_chain()

    return "Ok", 200

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['recipient_address', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    new_trans=transaction.create_transaction(values['recipient_address'],values['amount'])
    broadcast.broadcast_transaction(new_trans)
    return "Transaction sent",200



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

    #print(f'My port {data.myPort} ,Admin\'s port {data.adminPort}')
    #print(f'My publicKey {data.publicKey}')


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
