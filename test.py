import rsa
import data
from base64 import b64encode, b64decode
import json
import cryptodome


keysize = 2048
(public,private) = rsa.newkeys(keysize)


values={"key":public}
print (values)
print(type(values))
asString="{\"key\":"+str(public)+"}"


print(asString)
print(type(asString))


newValues=json.loads(asString)
print(newValues)
print(type(newValues))

msg1 = "Hello Tony, I am Jarvis!"
msg2 = "Hello Toni, I am Jarvis!"

encrypted = b64encode(rsa.encrypt(msg1.encode(), private))
decrypted = rsa.decrypt(b64decode(encrypted), private)
signature = b64encode(rsa.sign(msg1.encode(), private, "SHA-512"))
verify = rsa.verify(msg1.encode(), b64decode(signature), public)
print("OK")
