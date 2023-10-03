from core.models.user import UserModel
from core.models.transaction import TransactionModel,ToPayModel
from flask import jsonify, request
import pandas as pd

def createTransaction(current_user):
    data = request.get_json()

    new_txn = TransactionModel(name=data['name'], description=data['description'], paid_by=data['paid_by'], amount=data['amount'])
    split_between = data['split_between']
    try:
        new_txn.save_to_db()
    except:
        return {"message" : "Error saving txn"}, 401

    if data['expense'].lower() == 'equal':
        #validate_user
        for id in split_between:
            if not UserModel.find_by_id(id):
                return {"message" : "Invalid user id provided"}, 401
        if not data['amount']:
            return {"message" : "Amount not provided"}, 401
        each_share = round(float(data['amount']) / len(split_between),2)
        for id in split_between:
            to_pay = ToPayModel(user_to_pay_id=new_txn.paid_by,paying_user_id=id,amount=each_share,txn_id=new_txn.id)
            try:
                to_pay.save_to_db()
            except:
                return {"message": "Error saving individual share"}, 401

    return jsonify({"message": "New Txn is created!","response" : new_txn.json()})

def total_shares(current_user):
    amt_to_get_frm_user = ToPayModel.find_by_user_to_pay(current_user.id)
    data_list=[]
    for itm in amt_to_get_frm_user:
        data={}
        data['to_pay'] = itm.user_to_pay.email
        data['to_get_pay'] = itm.paying_user.email
        data['amount'] = itm.amount
        data_list.append(data)

    df = pd.DataFrame(data_list)
    df = df.groupby('to_get_pay')['amount'].sum().reset_index()

    return df.to_json(orient='records')
