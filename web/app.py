# app.py


import requests
from flask import Flask
from flask import request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
from datetime import datetime as dt



app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)


from models import *


@app.route('/yahoofinance/api/v1.0/insert_history', methods=['POST'])
def insert_finance_data():
    
    if not request.json or not 'company_name' in request.json:
        abort(jsonify(message="400 Bad Request"))
    
    company_name = request.json['company_name']

    # if company with this name is not in database, it creates data for new company
    if not bool(CompanyName.query.filter_by(name=company_name).first()):
        
        new_company = CompanyName(name=company_name,
                                  created_on=dt.now())
        db.session.add(new_company)
        db.session.commit()
        db.session.rollback()
        history_list = get_history_from_url(company_name=company_name)
        company = CompanyName.query.filter_by(name=company_name).first()

        insert_hist_value(fin_hist=history_list,
                          company=company,
                )
        
        return jsonify({'description': "A new company '{0}' is created and its financial history inserted".format(company_name),
                        'message':"200 Success Request"})
    
    # if company already in database
    company_obj = CompanyName.query.filter_by(name=company_name).first()
    already_inserted = CompanyFinancialHistory.query.filter_by(company_id=company_obj.id).all()
    # get history from finance.yahoo.com
    history_list = get_history_from_url(company_name=company_name)
    
    if (len(already_inserted) == len(history_list)):
        return jsonify({'description': "History is up to date",
                        'message':"201 Success Request"})
    
    elif(len(already_inserted) < len(history_list)):
        delta_history = history_list[len(already_inserted):]
        insert_hist_value(fin_hist=delta_history,
                          company=company_obj)
        return jsonify({'description': "{0} new data inserterted".format(len(delta_history)),
                        'message': "200 Success request"})
    else:
        return jsonify({'description': "Somethig wen't wrong",
                        'message':"201 Success Request"})

# returns list of fin history for the specific company_name
@app.route('/yahoofinance/api/v1.0/history/list', methods=['GET'])
def list_finance_data():
    
    if not request.json or not 'company_name' in request.json:
        abort(jsonify(message="400 Bad Request"))
    
    company_name = request.json['company_name']

    if not bool(CompanyName.query.filter_by(name=company_name).first()):
        return jsonify({'description': "No data for '{0}'".format(company_name),
                        'message':"201 Success Request"})
    
    company_obj = CompanyName.query.filter_by(name=company_name).first()
    already_inserted = CompanyFinancialHistory.query.filter_by(company_id=company_obj.id).all()
    
    if len(already_inserted) > 0:
        cols = ['date_of_insert', 'open', 'low', 'close', 'adj_close', 'volume']
        result = [{col: getattr(d, col) for col in cols} for d in already_inserted]
        return jsonify(json_list=result)

def insert_hist_value(fin_hist, company):
    """
    Insert list of historical entry to DB
    """
    try:
        for hist in fin_hist:
            new_hist = CompanyFinancialHistory( company_id=company.id,
                                                date_of_insert=hist.split(",")[0],
                                                open=float(hist.split(",")[1]),
                                                low=float(hist.split(",")[2]),
                                                close=float(hist.split(",")[3]),
                                                adj_close=float(hist.split(",")[4]),
                                                volume=int(hist.split(",")[-1])
            )
            db.session.add(new_hist)
            db.session.commit()
            db.session.rollback()
    
    except Exception as e:
        print(str(e))

def get_history_from_url(company_name=None):
    """
    Take comapany name as argument,
    query an url to get historical entries
    """
    if company_name:
        ## min date is an unix epoch 1970
        min_period = str(int(dt.timestamp(dt(1970,11,28, 23,55,59))))
        max_period = str(int(dt.timestamp(dt.now())))
        query_url = "https://query1.finance.yahoo.com/v7/finance/download/" + company_name
        params = {
            "period1": min_period,
            "period2":max_period,
            "interval":"1d",
            "events":"history",
            "includeAdjustedClose":"true"

        }

        try:
            response = requests.get(url=query_url, 
                                    params=params)
            content = response.content.decode("utf-8")
            return content.split()[2:]
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    app.run()
