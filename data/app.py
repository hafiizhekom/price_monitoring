import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
import datetime
import os
import json

class Data():

  def __init__(self, path=False):
    if path:
      self.db = TinyDB(path)
    else:
      self.db = TinyDB(os.getcwd()+"/db/db.json")

  def setUrl(self, url):
    now = datetime.datetime.now()

    Price = Query()
    curr_url = self.db.search(Price.url == str(url))
    if curr_url == []:
      self.db.insert(
        {
          "url": str(url),
          "price": {
            str(now): self.crawlPrice(url)
          }
        }
      )
      return True
    else:
      return False

  def getUrl(self):
    data_url = self.db.all()
    url = []
    for data in data_url:
      url.append(data['url'])
    return url

  def getPrice(self, url):
    Price = Query()
    curr_url = self.db.search(Price.url == str(url))
    if curr_url != []:
      return curr_url[0]['price']
    else:
      return {}

  def updatePrice(self, url, price):
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    Price = Query()
    curr_url = self.db.search(Price.url == str(url))
    if curr_url != []:
      curr_url[0]['price'][str(now)]=price
    self.db.update({'price': curr_url[0]['price']}, Price.url == str(url))

  def crawlPrice(self, url):
    req = requests.get(url)
    if req.status_code == 200:
      soup = BeautifulSoup(req.text, "html.parser")
      price = soup.find("meta", property="product:price:amount")['content']
      return price
    else:
      return None

  def crawlUrl(self, url):
    result = {}
    req = requests.get(url)
    if req.status_code == 200:
      soup = BeautifulSoup(req.text, "html.parser")

      price = soup.find("meta", property="product:price:amount")['content']
      title = soup.find("meta", property="og:title")['content']
      image = soup.find("meta", property="og:image")['content']
      description = soup.find("meta", property="og:description")['content']

      if description == "":
        description = soup.find('div', {'id': 'description'})
        description = description.p.span.get("data-sheets-value")
        description = json.loads(description)['2']

      result['title'] = title
      result['image'] = image
      result['price'] = price
      result['description'] = description

      return result
    else:
      result['title'] = ""
      result['image'] = ""
      result['price'] = 0
      result['description'] = ""
      return result


