import rsa
import data
from base64 import b64encode, b64decode


def initKeys():
    print('[*] Generating secret, please hang on.')

    keysize = 2048
    (data.publicKey, data.privateKey) = rsa.newkeys(keysize)

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
