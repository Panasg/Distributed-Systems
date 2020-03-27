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
    seed(1)
    keysize = 2048
    #(data.publicKey, data.privateKey) = rsa.newkeys(keysize)
    with data.lock:
        data.publicKey=str(data.myPort)*3


'''
# Generate keypair and store in global state
def generate_keypair():
    if (date.privateKeykey and data.publicKeykey) is not None:
        return

    rsa_keypair = RSA.generate(2048)

    with data.lock:
        state.privkey = rsa_keypair.exportKey('PEM').decode()
        state.pubkey = rsa_keypair.publickey().exportKey('PEM').decode()

        # Token is the sha of a part of the private key.
        state.token = SHA384.new(state.privkey[::2].encode()).hexdigest()


    
    signature = b64encode(rsa.sign(msg1.encode(), private, "SHA-512"))
    verify = rsa.verify(msg1.encode(), b64decode(signature), public)


    print(msg1.encode())

    try:
        other_verify=rsa.verify(msg2.encode(), b64decode(signature), public)
        print(other_verify)
    except:
        print("false verification")
    '''
