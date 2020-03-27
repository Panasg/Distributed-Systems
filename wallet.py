#import rsa
import data
from base64 import b64encode, b64decode

# seed the pseudorandom number generator
from random import seed
from random import random

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384

def initKeys():
    print('[*] Generating secret, please hang on.')

    keysize = 2048
    #(data.publicKey, data.privateKey) = rsa.newkeys(keysize)
    with data.lock:
        #data.publicKey=str(data.myPort)*3

        rsa_keypair = RSA.generate(2048)


        data.privateKey = rsa_keypair.exportKey('PEM').decode()
        data.publicKey = rsa_keypair.publickey().exportKey('PEM').decode()
