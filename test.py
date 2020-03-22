import rsa
import data
from base64 import b64encode, b64decode
import json


keysize = 2048
(public,private) = rsa.newkeys(keysize)
