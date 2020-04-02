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
import copy
# Instantiate the Node
app = Flask(__name__)

@app.route('/showYourData', methods=['POST'])
def show_it():
    with data.lock:

        for block in  data.blockchain.chain:
            print(block.asDictionary())

        for trans in data.current_transactions.values():
            print(trans.asDictionary())

        print(data.id)
        print(data.utxos)

        consensus_result=utilities.consensus()
    return "OK",200

@app.route('/benchmark', methods=['get'])
def benchmarks():
    if len(data.transactionTimes) ==0 or len(data.miningTimes)==0:
        return "No data",400
    averageTrans=sum(data.transactionTimes)/len(data.transactionTimes)
    averageMining=sum(data.miningTimes)/len(data.miningTimes)

    resp=f"Average Transaction Time: {averageTrans}\nAverage Mining Time: {averageMining}"
    return resp,200


@app.route('/cliShowMeYourState', methods=['GET'])
def show_it2():
    with data.lock:
        blockCh=[]
        transInChain=[]

        for block in  data.blockchain.chain:
            blockCh.append({'current':block.current_hash,'previous':block.previous_hash,'index':block.index})
            temp=[]
            for tr in block.transactions:
                temp.append(tr.id)
            transInChain.append(copy.deepcopy(temp))
        for i in range (1,len(data.blockchain.chain)):
            if data.blockchain.chain[i].previous_hash!=data.blockchain.chain[i-1].current_hash:
                print(f"Invalid chain in index {i}")

        current_transactions=[]
        for trans in data.current_transactions.values():
            current_transactions.append({'id':trans.id,'amount':trans.amount})

        body={
            "blockchain":blockCh,
            "current_transactions":current_transactions,
            "utxos":data.utxos
        }


        blockCh1=blockCh[:10]
        transInChain1=transInChain[:10]
        resp=f"Chain: {str(blockCh1)} \nLength: {len(blockCh)}\nCurrent trans: {str(current_transactions)}"\
            f"\nLength:{len(current_transactions)}\nUtxos: {str(data.utxos)}"\
            f"\nTransactions I serviced:{data.transactionsServiced}"\
            f"\n Trans ids in chain {transInChain1}"
    return resp,200

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
        data.current_transactions[trans_obj.id]=trans_obj
        if len(data.current_transactions)>=data.capacity:
            mining.mine()

        with data.chainLock:#πρεπει να ανανεωσουμε τα δεδομενα για το chain endpoint
            data.current_transactionsForCons=copy.deepcopy(data.current_transactions)
            data.utxosForCons=copy.deepcopy(data.utxos)

    return "transaction received",200

@app.route('/receiveABlock', methods=['POST'])
def receive_a_block():
    values = request.get_json()

    required = ['index', 'transactions', 'timestamp','nonce','previous_hash','current_hash']
    if not all(k in values for k in required):
        return 'Missing values', 400

    my_block=utilities.asObject(values,'block')
    if len(data.blockchain.chain)==0:
        with data.lock:
            for transaction in my_block.transactions:# πρεπει να κανουμε validate το genesis transaction
                transaction.validate_transaction()
            data.blockchain.chain.append(my_block)

            with data.chainLock:#πρεπει να ανανεωσουμε τα δεδομενα για το chain endpoint
                data.blockchainForCons=copy.deepcopy(data.blockchain)
                data.current_transactionsForCons=copy.deepcopy(data.current_transactions)
                data.utxosForCons=copy.deepcopy(data.utxos)

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


            for transaction in my_block.transactions:
                tran_id=transaction.id
                #if tran_id in data.transaction_pool:
                    #return "Transaction already in block",402
                for bl in data.blockchain.chain:# διατρεχουμε ολο το chain
                    for tr in bl.transactions:
                        if tr.id==tran_id:
                            if len(data.current_transactions)>=data.capacity:#ισως ηρθαν στην ουρα πολλα ακομα transactions
                                mining.mine()
                            return "Transaction already in block",402

                if  not  ( tran_id in data.current_transactions):
                    if len(data.current_transactions)>=data.capacity:#ισως ηρθαν στην ουρα πολλα ακομα transactions
                        mining.mine()
                    return "Unheard transaction in new  block",402
            #afairoyme osa exoyme koina sto current_transactions
            for trans in my_block.transactions:
                tran_id=trans.id
                data.current_transactions.pop(tran_id)
                #data.transaction_pool.append(trans.id)

            data.blockchain.chain.append(my_block)

            #for transId in utilities.getListOfKeys(data.current_transactions):
                #if transId in data.transaction_pool:
                    #data.current_transactions.pop(transId)

            if len(data.current_transactions)>=data.capacity:#ισως ηρθαν στην ουρα πολλα ακομα transactions
                mining.mine()

            with data.chainLock:#πρεπει να ανανεωσουμε τα δεδομενα για το chain endpoint
                data.blockchainForCons=copy.deepcopy(data.blockchain)
                data.current_transactionsForCons=copy.deepcopy(data.current_transactions)
                data.utxosForCons=copy.deepcopy(data.utxos)
                #data.transactionPoolForCons=copy.deepcopy(data.transaction_pool)
            return "Block added",200
            #data.utxos_copy=data.utxos[:]



    #2h to hash yparxei pio ba8eia sthn oyra
        for temp_blocks in reversed(data.blockchain.chain):
            if my_block.previous_hash==temp_blocks.current_hash:
                if len(data.current_transactions)>=data.capacity:#ισως ηρθαν στην ουρα πολλα ακομα transactions
                    mining.mine()
                #den kanoyme kati to aporriptoyme
                return "My chain is  not shorter,block rejected",403

    #3h to previous hash den yparxei mesa sthn lista mas
        #consensus
        print("I will call consensus Now")
        consensus_result=utilities.consensus()

        for transId in utilities.getListOfKeys(data.current_transactions):
            if transId in data.transaction_pool:
                data.current_transactions.pop(transId)

        with data.chainLock:#πρεπει να ανανεωσουμε τα δεδομενα για το chain endpoint
            data.blockchainForCons=copy.deepcopy(data.blockchain)
            data.current_transactionsForCons=copy.deepcopy(data.current_transactions)
            data.utxosForCons=copy.deepcopy(data.utxos)
            #data.transactionPoolForCons=copy.deepcopy(data.transaction_pool)

        if len(data.current_transactions)>=data.capacity:#ισως ηρθαν στην ουρα πολλα ακομα transactions
            mining.mine()
        return "consensus",consensus_result
            #an petyxei parnoyme chain, trans kai uxos



@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    with data.benchmarkLock:
        t1=time()

    values = request.get_json()
    required = ['recipient_address', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    new_trans=transaction.create_transaction(values['recipient_address'],values['amount'])
    broadcast.broadcast_transaction(new_trans)

    with data.benchmarkLock:
        data.transactionTimes.append(time()-t1)
        data.transactionsServiced=data.transactionsServiced+1

    return "Transaction sent",200



@app.route('/chain', methods=['GET'])
def full_chain():
    with data.chainLock:
        blockchainAsDiction=[block.asDictionary() for block in data.blockchainForCons.chain]
        transactionsAsDiction={}
        for transId in data.current_transactionsForCons:#για καθε key του dictionary
            transactionsAsDiction[transId] = data.current_transactionsForCons[transId].asDictionary()


        response = {
            'chain': blockchainAsDiction,
            'transactions':transactionsAsDiction,
            'utxos':data.utxosForCons,
            'length': len(blockchainAsDiction)#,
            #'pool':data.transactionPoolForCons
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
    parser.add_argument('-l', '--lastByte', default=1, type=int, help='my lastByte')#admin παντα στο 0

    args = parser.parse_args()

    data.myPort=port = args.port
    data.adminPort=args.admin
    data.myUrl=f"http://192.168.0.{str(args.lastByte)}:{data.myPort}"
    wallet.initKeys()

    data.blockchain = block_chain.Blockchain()


    myInfo={
        "url":data.myUrl,
        "publicKey":data.publicKey
    }
    if data.myPort!=data.adminPort:#expecting admin to be listening
        kwargs = {}
        kwargs['timeout'] = 1000
        setupResponse=requests.get(f'http://192.168.0.1:{data.adminPort}/setup',json=myInfo,**kwargs)#ston admin

    else:#admin is not listening yet
        setupNetwork.register(myInfo)



    app.run(host='0.0.0.0', port=port)
    print("After run")
