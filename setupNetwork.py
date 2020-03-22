import data
from flask import Flask, jsonify, request
import requests
import json
import threading
import time

tempNodes=[]
tempKeys=[]


def register(values):
    #print(json.loads(str(values)))


    nodes=values['nodes']
    publicKey=values['publicKey']
    print(f"Type of nodes {type(nodes)}")

    for node in [nodes]:
        tempNodes.append(node)
        print (f'Nodes so far {tempNodes}')
    tempKeys.append(publicKey)
    print(f"Keys so far {tempKeys}")

    data.connectedParticipants=data.connectedParticipants+1
    if data.numOfParticipants==data.connectedParticipants:#now we must send to everyone(including admin) all nodes
        x = threading.Thread(target=informEveryParticipant)
        x.start()




def informEveryParticipant():
    time.sleep(2)
    kwargs = {}
    kwargs['timeout'] = 5
    body = {"nodes":tempNodes}
    for node in tempNodes:
        print(node+"/nodes/register")
        response=requests.post(node+"/nodes/register",json=body,**kwargs)
        print(response.status_code)
        print(response.json)
