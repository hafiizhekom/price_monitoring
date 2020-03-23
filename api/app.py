from flask import Flask, jsonify, request
from data.app import Data
import datetime
app = Flask(__name__)
data = Data('../data/db/db.json')

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
    data_result = {}
    for url in data.getUrl():
        list_price = data.getPrice(url)
        max_price = list_price[max(k for k in list_price)]
        data_result[url] = {"current": data.crawlUrl(url), "last_price": {"date":max(k for k in list_price), "price":max_price}}

    result = {
        "response": True,
        "data": data_result
    }

    return result

@app.route('/data/detail', methods=['GET'])
def getDetail():
    url = request.args.get('url')
    data_result = {"current":data.crawlUrl(url), "price":data.getPrice(url)}

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


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)