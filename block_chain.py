import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
#from Crypto.PublicKey import RSA
from flask import Flask, jsonify, request
import requests
import wallet

import data
#import flask

class Blockchain:
    def __init__(self):

        self.chain = []



    def register_node(self, address,key):
        self.publicKeys.append(key)
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.append(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.append(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def print_chain(self):
        blockAsList=[]
        for bl in self.chain:
            blockAsList.append(bl.asDictionary())
        print (blockAsList)


    def imported_block(self, index, transactions,timestamp,proof,previous_hash,current_hash):
        block = {
            'index': index,
            'timestamp': timestamp,
            'transactions': transactions,
            'proof': proof,
            'previous_hash': previous_hash ,
            'current_hash':current_hash
        }
        self.current_transactions = []
        self.chain.append(block)
        return block



    @property
    def last_block(self):
        return self.chain[-1]
