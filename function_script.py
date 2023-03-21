import finnhub
import json
from pprint import pprint
import os
import configs
from flask import Flask, render_template, request, jsonify

API_KEY = configs.API_KEY

token = API_KEY
finnhub_client = finnhub.Client(api_key=token)

def pull_company_info(symbols):
    company_info = []
    for company in symbols:
        company_profile = finnhub_client.company_profile2(symbol=company)
        financials = finnhub_client.financials_reported(symbol=company, freq='quarterly')
        basic_financials = finnhub_client.company_basic_financials(company, 'all')

        json_fin = json.dumps(financials)
        json_fin = json.loads(json_fin)

        json_bf = json.dumps(basic_financials)
        json_bf = json.loads(json_bf)

        try: 
            ticker = company_profile['ticker']
        except:
            ticker = None
        try:
            sharesOutstanding = company_profile['shareOutstanding']
        except: 
            sharesOutstanding = None
        try:
            gaapNetIncome = json_fin['data'][0]['report']['ic'][6]['value']
        except:
            gaapNetIncome = None
        try:
            period = json_bf['series']['annual']['pe'][0]['period']
        except:
            period = None
        try:
            pe_ratio = json_bf['series']['annual']['pe'][0]['v']
        except:
            period = None

        # Handle non-serializable objects
        if ticker is None or sharesOutstanding is None or gaapNetIncome is None or period is None or pe_ratio is None:
            continue

        company_metric = {"name": ticker, "sharesOutstanding": (sharesOutstanding * 1000000), "gaapNetIncome": gaapNetIncome, "EPS": (gaapNetIncome/sharesOutstanding), "Period of PE": period, "PE Ratio": pe_ratio}
        company_info.append(company_metric)

    return company_info


def min_pe(company_info):
     min_pe = min(company_info, key=lambda x: x['PE Ratio'])
     return min_pe


def max_pe(company_info):
    max_pe = max(company_info, key=lambda x: x['PE Ratio'])
    return max_pe

