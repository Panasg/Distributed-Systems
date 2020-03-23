import rsa
import data
from base64 import b64encode, b64decode

# seed the pseudorandom number generator
from random import seed
from random import random

def initKeys():
    print('[*] Generating secret, please hang on.')
    seed(1)
    keysize = 2048
    #(data.publicKey, data.privateKey) = rsa.newkeys(keysize)
    data.publicKey=str(data.myPort)*3

    print(type(data.publicKey))
    '''
    signature = b64encode(rsa.sign(msg1.encode(), private, "SHA-512"))
    verify = rsa.verify(msg1.encode(), b64decode(signature), public)


    print(msg1.encode())

    try:
        other_verify=rsa.verify(msg2.encode(), b64decode(signature), public)
        print(other_verify)
    except:
        print("false verification")
    '''
