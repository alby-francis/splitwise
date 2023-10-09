from core.models.user import UserModel
from core.models.transaction import TransactionModel,ToPayModel
from flask import jsonify, request, json
import pandas as pd

def createTransaction(current_user):
    data = request.get_json()
    desc = data['description'] if data['description'] else None
    split_type = ['exact','percent','share']
    if not data['amount'] or not data['name'] or not data['paid_by']:
        return {"message": "Required fields are missing"}, 401

    new_txn = TransactionModel(name=data['name'], description=desc, paid_by=data['paid_by'], amount=data['amount'])

    if data['expense'].lower() == 'equal':
        if not data['split_equal']:
            return {"message" : "split_equal(dtype=list) key is required"}, 401
        split_between = data['split_equal']

        #validate_user
        try:
            validate_users(split_between)
        except Exception as e:
            return {"message": e}, 401

        each_share = round(float(data['amount']) / len(split_between),2)

        try:
            new_txn.save_to_db()
        except:
            return {"message": "Error saving txn"}, 401

        for id in split_between:
            if id != new_txn.paid_by:
                to_pay = ToPayModel(user_to_pay_id=new_txn.paid_by,paying_user_id=id,amount=each_share,txn_id=new_txn.id)
                try:
                    to_pay.save_to_db()
                except:
                    return {"message": "Error saving individual share"}, 401

    elif data['expense'].lower() in split_type:
        if not data['split_custom']:
            return {"message" : "split_custom (dtype=dict) key is required"}, 401

        try:
            all_users = [int(k) for k,v in data['split_custom'].items()]
            total = sum([float(v) for k,v in data['split_custom'].items()])
        except :
            return {"message": "Invalid user id"}, 401

        if data['expense'].lower() == 'exact' and total != float(data['amount']):
            return {"message": "Individual total and amount dont match"}, 401

        if data['expense'].lower() == 'percent' and total != 100:
            return {"message": "Individual percentage dont add up to 100"}, 401

        # validate_user
        try:
            validate_users(all_users)
        except Exception as e:
            return {"message": e}, 401

        try:
            new_txn.save_to_db()
        except:
            return {"message": "Error saving txn"}, 401


        for id in all_users:
            if id != new_txn.paid_by:
                if data['expense'].lower() == 'exact':
                    to_pay = ToPayModel(user_to_pay_id=new_txn.paid_by,paying_user_id=id,amount=float(data['split_custom'][str(id)]),txn_id=new_txn.id)
                elif data['expense'].lower() == 'percent':
                    amt = round(float(data['split_custom'][str(id)]) * float(data['amount']/100) ,2)
                    to_pay = ToPayModel(user_to_pay_id=new_txn.paid_by, paying_user_id=id,amount=amt, txn_id=new_txn.id)
                elif data['expense'].lower() == 'share':
                    amt = round(float(data['amount']/total) * data['split_custom'][str(id)], 2)
                    to_pay = ToPayModel(user_to_pay_id=new_txn.paid_by, paying_user_id=id, amount=amt,
                                        txn_id=new_txn.id)
                try:
                    to_pay.save_to_db()
                except:
                    return {"message": "Error saving individual share"}, 401

    return jsonify({"message": "New Txn is created!","response" : new_txn.json()})

def validate_users(users):
    for id in users:
        if not UserModel.find_by_id(id):
            raise Exception(f"No user found with {id}")

def total_shares(current_user):
    # To get payment
    amt_to_get_frm_user = ToPayModel.find_by_user_to_pay(current_user.id)

    get_payment_data_list = get_to_pay_dict_list(amt_to_get_frm_user)

    gp_df = pd.DataFrame(get_payment_data_list)
    #gp_df = gp_df.groupby('to_get_pay')['amount'].sum().reset_index()

    # to give payment
    amt_to_pay_to_user = ToPayModel.find_by_paying_user(current_user.id)

    to_pay_data_list = get_to_pay_dict_list(amt_to_pay_to_user)

    tp_df = pd.DataFrame(to_pay_data_list)
    tp_df['amount'] = -tp_df['amount']

    df = pd.concat([tp_df, gp_df], axis=0)

    df = df.groupby(['user_getting_paid','paying_user'])['amount'].sum().reset_index()
    #tp_df = tp_df.groupby('to_get_pay')['amount'].sum().reset_index()

    response = json.loads(df.to_json(orient='records'))
    for item in response:
        if item['amount'] < 0:
            temp = item['paying_user']
            item['paying_user'] = item['user_getting_paid']
            item['user_getting_paid']  = temp
    return {"message" : "Success", "response": response}, 201

def get_to_pay_dict_list(obj_list):
    data_list = []
    for itm in obj_list:
        data = {}
        data['paying_user'] = itm.user_to_pay.email
        data['user_getting_paid'] = itm.paying_user.email
        data['amount'] = itm.amount
        data_list.append(data)
    return data_list