from flask import Flask, jsonify, request
from data.app import Data
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
data = Data('data/db/db.json')

@app.route('/data', methods=['POST'])
def setUrl():
    url = request.form['url']
    if data.setUrl(url):
        result = {
            "response": True,
            "message":"Succes add url"
        }
        return result
    else:
        result = {
            "response": False,
            "message": "Fail add url"
        }
        return result


@app.route('/data', methods=['GET'])
def getAll():
    data_result = []
    for url in data.getUrl():
        list_price = data.getPrice(url)
        max_price = list_price[max(k for k in list_price)]
        data_result.append({"url": url, "detail": data.crawlUrl(url), "last_price": {"date":max(k for k in list_price), "price":max_price}})

    result = {
        "response": True,
        "data": data_result
    }

    return result

@app.route('/data/detail', methods=['GET'])
def getDetail():
    url = request.args.get('url')

    sumber_price = data.getPrice(url)
    price = []

    for date in sumber_price:
        price.append({"date": date, "price": sumber_price[date]})

    data_result = {"url": url,"detail":data.crawlUrl(url), "price":price}

    if url:
        result = {
            "response": True,
            "data": data_result
        }
        return result
    else:
        result = {
            "response": False,
            "message": "Data not found"
        }
        return result

@app.route('/')
def index():
    return "Powered by Flask 1.1.1"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)