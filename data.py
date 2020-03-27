import threading


myPort =None
adminPort=None
myUrl=None

publicKey=None
privateKey=None
id=None

blockchain=None
current_transactions={}#dictionary gia na briskoyme me bash to trans_id

allUrls=[]
allPublicKeys=[]

connectedParticipants=0

#aytes tis allazoyme gia na parametropoihsoyme to systhma mas
numOfParticipants=3

lock = threading.RLock()
