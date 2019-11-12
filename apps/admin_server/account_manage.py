# -*- coding: utf-8 -*-
import os
from flask import jsonify
from flasgger import swag_from
from . import admin_server
from utils.response import Response
from .models import Account, User, FundFlow, Pricing
from flask import request
import bcrypt
import logging
from datetime import datetime, date
from peewee import JOIN, fn, SQL
from plugins.user_plugin import encode_auth_token, get_jwt_user
base_dir = os.path.dirname(__file__)
account_banance_yml_path = os.path.join(base_dir, "docs/account_banance.yml")
account_history_yml_path = os.path.join(base_dir, "docs/account_history.yml")
daily_consumption_yml_path = os.path.join(base_dir, "docs/daily_consumption.yml")

@admin_server.route('/account_balance', endpoint='account_banance', methods=['GET'])
@swag_from(account_banance_yml_path, endpoint='admin_server.account_balance', methods=['GET'])
def account_banance():
    """
    账户余额
    :return:
    """
    res = Response()
    payload = get_jwt_user()
    user_id = payload['user_id']
    amount = Account \
                .select(Account.amount) \
                .join(User, JOIN.LEFT_OUTER, on=(User.account_id == Account.id))\
                .where(User.id == user_id)
    try:
        amount = amount.dicts()
        res.Code = 200
        res.Message = "success"
        res.Result = amount[0]
    except:
        res.Code = 400
        res.Message = "no account info"
    return jsonify(res.object_to_dict())

@admin_server.route('/fund_flow', endpoint='fund_flow', methods=['POST'])
@swag_from(account_history_yml_path, endpoint='admin_server.fund_flow', methods=['POST'])
def fund_flow():
    """
    用户账户充值垫付取消的历史记录, 可以根据date和type进行筛选
    :return:
    """
    res = Response()
    payload = get_jwt_user()
    account_id = payload['account_id']
    input_json = request.json
    try:
        fund_flow = FundFlow.select().where(FundFlow.account_id == account_id)
        if fund_flow is not None:
            pricing = Pricing.get_or_none(Pricing.account_id == account_id)
            balance_type = None
            if pricing:
                balance_type = pricing.currency
            date_start = input_json.get("date_start", "")
            date_end = input_json.get("date_end", "")
            if date_start and date_end:
                fund_flow = fund_flow.where(FundFlow.created_at.between(date_start, date_end))
            type = input_json.get("fund_type", "")
            if type:
                fund_flow = fund_flow.where(FundFlow.fund_type == type)

            page_number = input_json.get("page_number", 1)
            length = input_json.get("length", 20)
            fund_flow = fund_flow.paginate(page_number, length)

            datas = []
            for fund_flow in fund_flow:
                data = {
                    "id": fund_flow.id,
                    "time": fund_flow.created_at,
                    "type": fund_flow.fund_type,
                    "balance_type": balance_type,
                    "amount": fund_flow.amount,
                    "balance": fund_flow.remain_amount,
                    "remark": fund_flow.fund_detail
                }
                datas.append(data)
            res.Code = 200
            res.Message = "success"
            res.Result = datas
        else:
            res.Code = 401
            res.Message = "no have permission"
        return jsonify(res.object_to_dict())
    except Exception as e:
        res.Code = 500
        res.Message = "Interval Error"
        return jsonify(res.object_to_dict())

@admin_server.route('/daily_consumption', endpoint='daily_consumption', methods=['POST'])
@swag_from(daily_consumption_yml_path, endpoint='admin_server.daily_consumption', methods=['POST'])
def daily_consumption():
    """
    用户日消费历史
    :return:
    """
    res = Response()
    payload = get_jwt_user()
    account_id = payload['account_id']
    input_json = request.json
    try:
        sql_res = FundFlow\
            .select(
                SQL('DATE(t2.created_at) AS date'),
                Pricing.currency.alias("balance_type"),
                fn.SUM(FundFlow.amount).alias("daily_consumption"),
                fn.MIN(FundFlow.remain_amount).alias("daily_balance")
                )\
            .join(Pricing, JOIN.LEFT_OUTER, on=(Pricing.account_id == account_id))\
            .where((FundFlow.account_id == account_id) & (FundFlow.fund_type == 2))\
            .order_by(FundFlow.created_at.desc())
        if sql_res is not None:
            date_start = input_json.get("date_start", "")
            date_end = input_json.get("date_end", "")
            if date_start and date_end:
                sql_res = sql_res\
                    .where(FundFlow.created_at.between(date_start, date_end)).group_by(SQL('date'))
            else:
                sql_res = sql_res.group_by(SQL('date'))
            print(sql_res)
            page_number = input_json.get("page_number", 1)
            length = input_json.get("length", 20)
            sql_res = sql_res.paginate(page_number, length)
            fund_flows = sql_res.dicts()
            datas = []
            for fund_flow in fund_flows:
                # datetime格式转化为字符串格式
                date = (fund_flow['date']).strftime('%Y-%m-%d')
                data = {
                    "date": date,
                    "daily_consumption": fund_flow['daily_consumption'],
                    "balance_type": fund_flow['balance_type'],
                    "daily_balance": fund_flow['daily_balance']
                }
                datas.append(data)
            res.Code = 200
            res.Message = "success"
            res.Result = datas
        else:
            res.Code = 401
            res.Message = "no have permission"
        return jsonify(res.object_to_dict())
    except Exception as e:
        res.Code = 500
        res.Message = "Interval Error. %s"%e
        return jsonify(res.object_to_dict())




# from playhouse.shortcuts import model_to_dict
# from flask import Response, make_response
# import csv
# from io import StringIO
# from utils.flask_json_encode import JSONEncoder
# import json

# @admin_server.route('/test_paginate', endpoint='test_paginate', methods=["GET"])
# def test_paginate():
    # args = request.json
    # start = args.get("start", 0)
    # length = args.get("length", 10)
    # res = FundFlow.select().where(FundFlow.account_id == 1).order_by(FundFlow.created_at).paginate(2, 10)
    # datas = []
    # for fund_flow in res:
    #     ff = JSONEncoder().encode(model_to_dict(fund_flow))
    #     data = json.loads(ff)
    #     datas.append(data)
    #
    # print("进来啦！！！")
    # print("datas", datas)
    # Response.set_header()
    # response.set_header('Content-Type', 'text/csv')
    # response.set_header('Content-Disposition',
    #                     'attachment; filename="reconciliation_remit.csv"')
    # with StringIO() as csv_file:
    #     fields = ('id', 'account_id', 'fund_type', 'fund_detail',
    #               'amount', 'remain_amount', 'pricing_id', 'request_id', 'created_at')
    #     w = csv.DictWriter(csv_file, fields, extrasaction='ignore')
    #     w.writeheader()
    #     w.writerows(datas)
    #     data = csv_file.getvalue().encode('utf8', 'ignore').decode()
    #     resp = make_response("这是一条测试数据")
    #     resp.status = "222"
    #     resp.headers["Content-Type"] = "text/csv"
    #     resp.headers["Content-Disposition"] = 'attachment; filename="reconciliation_remit.csv"'
    #
    #     return resp

# @admin_server.route('/downloadcsv', endpoint='test_paginate', methods=["GET"])
# def download_csv():
#     request.get_dict(field_name='file')

