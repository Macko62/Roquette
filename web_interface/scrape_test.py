import pandas as pd
import requests
from json import loads
from bs4 import BeautifulSoup

stophere = True
s=requests.Session()
# s.auth=('DISP294','S8z~v*Sxp!D6Zf:D')
# s.cert=('c:/Apache24/conf/Roquette_inter_full.cer')
r=s.get('http://159.89.182.128').text
# s.config['keep_alive'] = False
soup=BeautifulSoup(r,"lxml")
data=pd.read_json(soup.pre.text)
#data=loads(str(data))
# df=df_list[0].head()
# return [x for x in df.values]
# r = requests.get(url, headers={'Connection':'close'})