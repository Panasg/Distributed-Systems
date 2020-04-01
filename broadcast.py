import data
from flask import Flask, jsonify, request
import requests
import json
import threading
import time


def broadcast_transaction(new_trans):
    kwargs = {}
    kwargs['timeout'] = 25
    trans_dict=new_trans.asDictionary()

    try:#αρχικα το στελνω στον εαυτο μου
        response=requests.post(data.myUrl+"/receive_transaction",json=trans_dict,**kwargs)
    except requests.exceptions.Timeout:
        print(f'broadcast: Request {data.myUrl}/receive_transaction timed out')

    neighbours = [a for a in data.allUrls if a!=data.myUrl]
    for node in neighbours:
        try:
            response=requests.post(node+"/receive_transaction",json=trans_dict,**kwargs)
        except requests.exceptions.Timeout:
            print(f'broadcast: Request {node}/receive_transaction timed out')
    return



def broadcast_a_block(block):
    kwargs = {}
    kwargs['timeout'] = 25

    try:#αρχικα το στελνω στον εαυτο μου
        response=requests.post(data.myUrl+"/receiveABlock",json=block.asDictionary(),**kwargs)
        print ( response.text)
    except requests.exceptions.Timeout:
        print(f'broadcast: Block {data.myUrl}/receiveABlock timed out')

    neighbours = [a for a in data.allUrls if a!=data.myUrl]
    for node in neighbours:
        try:
            response=requests.post(node+"/receiveABlock",json=block.asDictionary(),**kwargs)
            print ( response.text)
        except requests.exceptions.Timeout:
            print(f'broadcast: Block {node}/receiveABlock timed out')
    return

        #print(response.status_code)
