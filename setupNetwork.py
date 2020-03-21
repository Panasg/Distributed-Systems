import data
from flask import Flask, jsonify, request
import requests
import json
import threading
import time

tempNodes=[]


def register(nodes):
    for node in nodes:
        tempNodes.append(node);
        print (f'Nodes so far {tempNodes}')
    data.connectedParticipants=data.connectedParticipants+1
    if data.numOfParticipants==data.connectedParticipants:#now we must send to everyone(including admin) all nodes
        x = threading.Thread(target=informEveryParticipant)
        x.start()




def informEveryParticipant():
    time.sleep(2)
    kwargs = {}
    kwargs['timeout'] = 5
    for node in tempNodes:
        print(node+"/nodes/register")
        body={"nodes":tempNodes}
        print(body)
        response=requests.post(node+"/nodes/register",json=body,**kwargs)
        print(response.status_code)
