import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, request
import requests
#import flask
import threading

import block_chain
import data
import setupNetwork
import wallet
import broadcast


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain=None


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/receiveATransaction', methods=['POST'])
def receive_a_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount','index']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # Create a new Transaction
    blockchain.validate_transaction(values)

    indexOfBlock = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'],values['index'])
    print(f"Current Transactions {blockchain.current_transactions}")
    response = {'message': f'Transaction will be added to Block {indexOfBlock}'}
    return str(response), 200

@app.route('/receiveABlock', methods=['POST'])
def receive_a_block():
    values = request.get_json()
    required = ['index', 'transactions', 'timestamp','proof','previous_hash','current_hash']
    if not all(k in values for k in required):
        return 'Missing values', 400
    my_block = blockchain.imported_block(values['index'], values['transactions'], values['timestamp'],values['proof'],values['previous_hash'],values['current_hash'])
    print(f"Current Blocks {blockchain.chain}")
    response = {'message': f'Block will be added {my_block}'}
    return str(response), 200


@app.route('/newTransaction', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = [ 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    body={
        'sender': data.publicKey,
        'recipient': values['recipient'],
        'amount': values['amount'],
        'index':max(data.nextIndex,data.temp_nextIndex)
    }
    data.temp_nextIndex=max(data.nextIndex,data.temp_nextIndex)+1
    #data.nextIndex=data.nextIndex++

    x = threading.Thread(target=broadcast.broadcast_a_transaction,args=(blockchain,body))
    x.start()

    return "OK",200
    x.join()



@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return str(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    print("I am getting register request")
    values = request.get_json()

    nodes = values.get('nodes')
    keys=values.get('publicKeys')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for i in range (0,len(nodes)):
        blockchain.register_node(nodes[i],keys[i])



    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
        'total_keys': list(blockchain.publicKeys),
    }

    return "Ok", 200

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


@app.route('/setup', methods=['GET'])
def setup():

    if data.myPort!=data.adminPort:
        res={"Message":"I Ain't admin"}
        return jsonify(res),200
    else:
        values=request.get_json()
        res={"Message":"Wait for everybodt to start"}
        setupNetwork.register(values,blockchain)

    return "OK",200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-a', '--admin', default=5000, type=int, help='port of admin')
    args = parser.parse_args()

    data.myPort=port = args.port
    data.adminPort=args.admin
    wallet.initKeys()
    blockchain = block_chain.Blockchain()
    #wallet.initKeys()
    print(f'My port {data.myPort} ,Admin\'s port {data.adminPort}')
    print(f'My publicKey {data.publicKey}')

    if data.myPort!=data.adminPort:#expecting admin to be listening
        myInfo={
            "nodes":[f"http://localhost:{data.myPort}"],
            "publicKey":data.publicKey
        }
        kwargs = {}
        kwargs['timeout'] = 5
        setupResponse=requests.get(f'http://localhost:{data.adminPort}/setup',json=myInfo,**kwargs)
        #print(f"Setup Response {setupResponse}")
    else:#admin is not listening yet
        myInfo={
            "nodes":[f"http://localhost:{data.myPort}"],
            "publicKey":data.publicKey
        }
        setupNetwork.register(myInfo,blockchain)



    app.run(host='0.0.0.0', port=port)
    print("After run")
