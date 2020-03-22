#from Crypto.PublicKey import RSA
#from Crypto.Hash import SHA384
'''
import pycrypto

publicKey
privateKey
token


def initKeys():
    rsa_keypair = RSA.generate(2048)
    privateKeyy = rsa_keypair.exportKey('PEM').decode()
    publicKey = rsa_keypair.publickey().exportKey('PEM').decode()

    # Token is the sha of a part of the private key.
    token = SHA384.new(state.privkey[::2].encode()).hexdigest()
'''
