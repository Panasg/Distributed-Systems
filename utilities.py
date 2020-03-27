import hashlib

def hashStringToString(stringToBeHashed):#dexetai string kai gyrnaei to hash toy ws string
    bytesOfString=stringToBeHashed.encode()
    hash_object = hashlib.md5(bytesOfString)
    digest=hash_object.hexdigest()
    return digest
