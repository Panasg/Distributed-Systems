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
import mining
# Instantiate the Node
app = Flask(__name__)

@app.route('/showYourData', methods=['POST'])
def show_it():
    print("I will show")
    with data.lock:

        for block in  data.blockchain.chain:
            print(block.asDictionary())

        for trans in data.current_transactions.values():

            print(trans.asDictionary())

        print(data.id)
        print(data.utxos)
    return "OK",200

@app.route('/receive_transaction', methods=['POST'])
def receive_transaction():

    values=request.get_json()
    required = ['sender', 'recipient', 'amount','timestamp', 'inputs','outputs', 'id', 'signature']
    if not all(k in values for k in required):

        return 'Missing values', 400

    trans_obj=utilities.asObject(values,"transaction")

    retValue=trans_obj.verify_signature()
    if not retValue:
        return "Invalid signature",201

    retValue=trans_obj.validate_transaction()
    if not retValue:
        return "Invalid transaction",201

    with data.lock:
        #print(f"type of elem in current tras {type(trans_obj)}")
        print(data.current_transactions)
        #print(f"i reached the capacity: {data.capacity}")
        data.current_transactions[trans_obj.id]=trans_obj
        print(data.current_transactions)
        print(len(data.current_transactions))
        if len(data.current_transactions)>=data.capacity:
            mining.mine()
    #print("AFTER SIGNATURE")
    return "transaction received",200

@app.route('/receiveABlock', methods=['POST'])
def receive_a_block():
    values = request.get_json()
    print(" I AM HERE ")
    required = ['index', 'transactions', 'timestamp','nonce','previous_hash','current_hash']
    if not all(k in values for k in required):
        return 'Missing values', 400

    my_block=utilities.asObject(values,'block')
    if len(data.blockchain.chain)==0:
        with data.lock:
            for transaction in my_block.transactions:
                transaction.validate_transaction()
            data.blockchain.chain.append(my_block)
            #print(data.utxos)
            data.utxos_copy=data.utxos[:]
        return "GenesisBlock added",200

    # to hash einai ypologismeno swsta
    if  my_block.hash()!=my_block.current_hash:
        return "Wrong Hash",400

    # to hash exei thn swsth morfh
    if mining.valid_proof(my_block) ==False:
        return "Invalid proof",401

    #1h to hash einai idio me to prohgoymeno hash, shmainei pws oi alysides symfvnoyn
    with data.lock:
        if  my_block.previous_hash==(data.blockchain.chain[-1]).current_hash:
            #pairnoyme ta utxos opws htan sto prohgoymeno block
            #data.utxos=data.utxos_copy[:]
            #kanoyme ena ena validate ta transactions san na ta vlepoyme prwth fora
            for transaction in my_block.transactions:
                tran_id=transaction.id
                if  not  ( tran_id in data.current_transactions):
                    return "unheard transaction in new  block",402
            #afairoyme osa exoyme koina sto current_transactions
            for trans in my_block.transactions:
                tran_id=trans.id
                data.current_transactions.pop(tran_id)
            data.blockchain.chain.append(my_block)
            return "Block added",200
            #data.utxos_copy=data.utxos[:]



    #2h to hash yparxei pio ba8eia sthn oyra
        for  temp_blocks in reversed(data.blockchain.chain):
            if my_block.previous_hash==temp_blocks.current_hash:
                #den kanoyme kati to aporriptoyme
                return "My chain is  not shorter,block rejected",403

    #3h to previous hash den yparxei mesa sthn lista mas
        #consensus
        consensus_result=utilities.consensus()
        return "consensus",consensus_result
            #an petyxei parnoyme chain, trans kai uxos

    #print(f"Current Blocks :")
    #data.blockchain.print_chain()

    

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
        'transactions':data.blockchain.transactions,
        'utxos':data.utxos,
        'length': len(data.blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/show_balance',methods=['GET'])
def show_balance():
    with data.lock:
        allMoney=sum(data.utxos[data.id].values())
    return str(allMoney),200

@app.route('/view_transactions', methods=['GET'])
def view_transactions():
    with data.lock:
        last_block=data.blockchain.chain[-1]
        listOfDicts=[]
        for trans in last_block.transactions:
            listOfDicts.append(trans.asDictionary())

    return str(listOfDicts),200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    print("I am getting register request")
    values = request.get_json()

    setupNetwork.saveNodes(values)
    return "ok",200

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
