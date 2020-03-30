import threading


myPort =None
adminPort=None
myUrl=None

publicKey=None
privateKey=None
id=None

blockchain=None
current_transactions={}#dictionary για να τα βρισκουμε με βαση το id

allUrls=[]
allPublicKeys=[]

utxos=[]

hasReceivedGenesisBlock=False
connectedParticipants=0

#αλλάζουμε αυτες τις τιμές για να παραμετροποι΄ήσουμε το συστημά μας
numOfParticipants=3
capacity=3
difficulty=4

lock = threading.RLock()# ώστε καθε νημα που έχει προσβαση στις ανώτερες τιμές να εχει ατομική προσβαση

#
miningLock=threading.RLock()# ώστε τα νήματα που κανουν mine να κάνουν Mine στην σειρά
someoneIsMining=False
