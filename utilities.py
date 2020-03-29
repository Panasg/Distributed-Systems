import hashlib
import  transaction
import block

def hashStringToString(stringToBeHashed):#dexetai string kai gyrnaei to hash toy ws string
    bytesOfString=stringToBeHashed.encode()
    hash_object = hashlib.md5(bytesOfString)
    digest=hash_object.hexdigest()
    return digest

def asDictionary(an_object,kind):

    tempList=[]
    if kind=='block':
        for i in an_object.transactions:
            tempList.append(asDictionary(i,"transaction"))
        tempDict={
        "index":an_object.index,
        "timestamp":an_object.timestamp,
        "transactions":tempList,
        "nonce":an_object.nonce,
        "current_hash":an_object.current_hash,
        "previous_hash":an_object.previous_hash,
                            }
    else:
        tempDict={
            "sender":an_object.sender,
            "recipient":an_object.recipient,
            "amount":an_object.amount,
            "timestamp":an_object.timestamp,
            "inputs":an_object.inputs,
            "outputs":an_object.outputs,
            "id":an_object.id,
            "signature":an_object.signature

        }
    return tempDict


def asObject(a_dictionary,kind):
    b=a_dictionary
    if kind=='block':
        temp_trans_list=[]
        for trans_dict in a_dictionary['transactions']:
            temp_trans_list.append(asObject(trans_dict,"transaction"))
        tempBlock=block.block(b['index'], b['timestamp'],temp_trans_list ,b['nonce'], b['current_hash'], b['previous_hash'])
        return tempBlock
    return transaction.transaction(b['sender'], b['recipient'], b['amount'],b['timestamp'], b['inputs'],b['outputs'], b['id'], b['signature'])


def getListOfKeys(dict):#παιρνει dict και γυρνα λιστα με ολα τα κλειδια του
    list = []
    for key in dict.keys():
        list.append(key)

    return list

def consensus():
    replaced = resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': data.blockchain.chain
        }
        status_code=500#replaced
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': data.blockchain.chain
        }
        status_code=200#not replaced
    return status_code

def resolve_conflicts():
    neighbours = data.allUrls
    new_chain = None

    # We're only looking for chains longer than ours
    max_length = len(data.blockchain.chain)

    # Grab and verify the chains from all the nodes in our network
    for node in neighbours:
        response = requests.get(f'{node}/chain')

        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            # Check if the length is longer and the chain is valid
            if length > max_length and valid_chain(chain):
                max_length = length
                new_chain = chain

    # Replace our chain if we discovered a new, valid chain longer than ours
    if new_chain:
        data.blockchain.chain = new_chain
        return True

    return False

def valid_chain(chain):
    tempChain=[]
    for blockAsDict in chain:
        tempChain.append(block.createBlockFromDictionary(blockAsDict))

    i=0
    for block in tempChain[1:]:
        i=i+1
        if not mining.valid_proof(block):
            return False
        if block.previous_hash!=tempChain[i-1].current_hash:
            return False
    return True
