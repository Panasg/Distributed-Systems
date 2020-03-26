import data
from flask import Flask, jsonify, request
import requests
import json
import threading
import time
import broadcast

tempNodes=[]
tempKeys=[]


def register(values,blockchain):
    #print(json.loads(str(values)))


    nodes=values['nodes']
    publicKey=values['publicKey']
    print(f"Type of nodes {type(nodes)}")

    for node in nodes:
        tempNodes.append(node)
        #print (f'Nodes so far {tempNodes}')
    tempKeys.append(publicKey)
    #print(f"Keys so far {tempKeys}")
    global my_chain
    my_chain=blockchain
    data.connectedParticipants=data.connectedParticipants+1
    if data.numOfParticipants==data.connectedParticipants:#now we must send to everyone(including admin) all nodes
        x = threading.Thread(target=informEveryParticipant)
        x.start()





def informEveryParticipant():
    time.sleep(2)
    kwargs = {}
    kwargs['timeout'] = 25
    genesis_block=my_chain.chain[0]
    my_chain.chain=[]
    body = {"nodes":tempNodes,
            "publicKeys":tempKeys}
    for node in tempNodes:
        print(node+"/nodes/register")
        response=requests.post(node+"/nodes/register",json=body,**kwargs)
        print(response.status_code)
    broadcast.broadcast_a_block(genesis_block,my_chain)
    #print (my_chain.nodes)
    # print(my_chain.publicKeys)

    for key in my_chain.publicKeys:
        if key!=data.publicKey:
            trans_body = {"recipient":key,"amount":100}
            response=requests.post('http://localhost:'+str(data.myPort)+'/newTransaction',json=trans_body,**kwargs)

        #print(response.text)
