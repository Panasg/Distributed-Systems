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


def StartMining():
    kwargs = {}
    kwargs['timeout'] = 25
    response=requests.get("http://localhost:"+str(data.myPort)+"/nodes/resolve")
    response=requests.get('http://localhost:'+str(data.myPort)+'/mine',**kwargs)
