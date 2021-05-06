import requests
x=requests.get('http://192.168.0.200:8000/')
data=x.json()
print(len(data))