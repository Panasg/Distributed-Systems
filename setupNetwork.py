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

    
    with data.lock:
        data.connectedParticipants=data.connectedParticipants+1
        if data.numOfParticipants==data.connectedParticipants:#now we must send to everyone(including admin) all nodes
            x = threading.Thread(target=informEveryParticipant)
            x.start()
    return





def informEveryParticipant():#only executed by admin
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

    genBlock=block.createGenesisBlock([genTrans])
    broadcast.broadcast_a_block(genBlock)

    for key in data.allPublicKeys:
        if key!=data.publicKey:#οχι σε μενα
            index=data.allPublicKeys.index(key)

            requestBody={
                'recipient_address':index,
                'amount':100
            }
            response=requests.post('http://localhost:'+str(data.myPort)+'/new_transaction',json=requestBody,**kwargs)
            print(f"Participant {index} got its money")
    return

def saveNodes(values):#executed by every participant
    data.allUrls=values['nodes']
    data.allPublicKeys=values['publicKeys']
    data.id=values['yourId']
    for i in range (0,len(data.allUrls)):
        data.utxos.append({})
    print("My id is "+str(data.id))

    return
