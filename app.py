import finnhub
import json
from pprint import pprint
import os
import configs
from flask import Flask, render_template, request, jsonify
from function_script import pull_company_info

API_KEY = configs.API_KEY

token = API_KEY
finnhub_client = finnhub.Client(api_key=token)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/company_info', methods=['POST'])
def company_info():
    symbol = request.json['symbol']
    company_info = pull_company_info([symbol])
    return jsonify(company_info)

if __name__ == '__main__':
    app.run(debug=True)

