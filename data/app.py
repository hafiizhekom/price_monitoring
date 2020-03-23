import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
import datetime
import os
class Data():

  def __init__(self, path=False):
    if path:
      self.db = TinyDB(path)
    else:
      self.db = TinyDB(os.getcwd()+"db/db.json")

  def getUrl(self):
    data_url = self.db.all()
    url = []
    for data in data_url:
      url.append(data['url'])
    return url

  def updatePrice(self, url, price):
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    Price = Query()
    curr_url = self.db.search(Price.url == str(url))
    if curr_url != []:
      curr_url[0]['price'][str(now)]=price
    self.db.update({'price': curr_url[0]['price']}, Price.url == str(url))
    print(self.db.all())

  def crawlPrice(self, url):
    req = requests.get(url)
    if req.status_code == 200:
      soup = BeautifulSoup(req.text, "html.parser")
      price = soup.find("meta", property="product:price:amount")['content']
      return price
    else:
      return None