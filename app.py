  
 #This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json,csv,time
import os.path

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  # https://pro.coinmarketcap.com/account/
  # you can get that from here
  'X-CMC_PRO_API_KEY': 'abf52351-f0cb-4233-849f-bf948c944ace',
}

session = Session()
session.headers.update(headers)
# it will extract this coin prices
# BTC,ETH,BCH,XMR,DASH,FIL,BAT,ZRX,REP,KNC
l = ['BTC','ETH','BCH','XMR','DASH','FIL','BAT','ZRX','REP','KNC']

while True:
  print("\n\n")
  print("="*50)
  print("info : starting...")

  if os.path.isfile('file.csv'):
      print ("info : File already exist")
  else:
      with open("file.csv","w+",newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(l)
      print ("info : File not exist... will create new file")

  rates = []

  print("info : Wait till data get loaded in the file...")

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    data = data['data']
    
    for a in data:
      for d in l:
        if(a['symbol'] == d ):
          rate = a['quote']['USD']['price']
          rates.append(rate)

    with open('file.csv',"a+",newline='', encoding='utf-8') as f:
      writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(rates)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


  print("success: Complete...")
  time.sleep(600)