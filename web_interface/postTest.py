import requests
import datetime

urlPut='http://127.0.0.1:8000/put/'
urlGet='http://127.0.0.1:8000/get/'
myData={
    'msgNum':12,
    'tuNumExt':6100000000,
    'door':'DRM7',
    'userOverride':False}
#x=requests.put(urlPut,myData)
#x=requests.get(urlGet)
for i in range(1,13):
    myData['msgNum']=i
    myData['tuNumExt']=6100000000+i*2
    x=requests.put(urlPut,myData)
    delta=0
    while x.status_code!=201:
        delta+=1
        if delta>=10_000: break
x=requests.get(urlGet)
print(x.json())