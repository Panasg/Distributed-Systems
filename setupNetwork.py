from flask import Flask, jsonify, request
import requests
import json
import threading
import time

import broadcast
import transaction
import block
import data


tempNodes=[]
tempKeys=[]



def register(values):#only executed by admin
    node=values['url']
    publicKey=values['publicKey']

    tempNodes.append(node)
    tempKeys.append(publicKey)

    #print(f"Keys so far {tempKeys}")
    with data.lock:
        data.connectedParticipants=data.connectedParticipants+1
        if data.numOfParticipants==data.connectedParticipants:#now we must send to everyone(including admin) all nodes
            x = threading.Thread(target=informEveryParticipant)
            x.start()
    return





def informEveryParticipant():#only executed by admin

    print ("I should inform now everyone")


    time.sleep(2)
    kwargs = {}
    kwargs['timeout'] = 25

    body = {"nodes":tempNodes,
            "publicKeys":tempKeys,
            }
    for i in range (0,len(tempNodes)):
        body["yourId"]=i
        response=requests.post(tempNodes[i]+"/nodes/register",json=body,**kwargs)


    genTrans=transaction.createGenesisTransaction()
    #print (genTrans.asDictionary())
    genBlock=block.createGenesisBlock([genTrans])
    broadcast.broadcast_a_block(genBlock)
    data.blockchain.print_chain()
    #print (genBlock.asDictionary())
    return

    broadcast.broadcast_a_block(genesis_block,my_chain)


    for key in my_chain.publicKeys:
        if key!=data.publicKey:
            trans_body = {"recipient":key,"amount":100}
            response=requests.post('http://localhost:'+str(data.myPort)+'/newTransaction',json=trans_body,**kwargs)

def saveNodes(values):#executed by every participant
    #print(values)
    data.allUrls=values['nodes']
    data.allPublicKeys=values['publicKeys']
    data.id=values['yourId']

    print("My id is "+str(data.id))

    return
