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

'''
def proof_of_work(self, last_block):
    last_proof = last_block['proof']
    last_hash = self.hash(last_block)

    proof = 0
    while self.valid_proof(last_proof, proof, last_hash) is False:
        proof += 1

    return proof


def valid_proof(last_proof, proof, last_hash):
    guess = f'{last_proof}{proof}{last_hash}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"


def resolve_conflicts(self):
    neighbours = self.nodes
    new_chain = None

    # We're only looking for chains longer than ours
    max_length = len(self.chain)

    # Grab and verify the chains from all the nodes in our network
    for node in neighbours:
        response = requests.get(f'http://{node}/chain')

        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            # Check if the length is longer and the chain is valid
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain

    # Replace our chain if we discovered a new, valid chain longer than ours
    if new_chain:
        self.chain = new_chain
        return True

    return False

'''
