# -*- coding: utf-8 -*-
import os
from flask import jsonify
from flasgger import swag_from
from . import admin_server
from utils.response import Response
from apps.models import Account, User, FundFlow, Pricing
from flask import request
from peewee import JOIN, fn, SQL
from plugins.user_plugin import get_jwt_user

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
        res.Result = {
            "data": amount[0]
        }
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
            else:
                fund_flow = fund_flow.where(FundFlow.fund_type.in_([4, 5, 6]))
            total_num = len(fund_flow)
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
            res.Result = {
                "data": datas,
                "total": total_num
            }
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
                SQL('DATE(t2.created_at)')
                    .alias("date"),
                Pricing.currency
                    .alias("balance_type"),
                fn.SUM(FundFlow.amount)
                    .alias("daily_consumption"),
                SQL('( SELECT remain_amount FROM fund_flow WHERE fund_flow.id = MAX( t2.id ) )')
                    .alias("daily_balance")
                )\
            .join(Pricing, JOIN.LEFT_OUTER, on=(Pricing.account_id == account_id))\
            .where((FundFlow.account_id == account_id) & (FundFlow.fund_type == 2))\
            .order_by(FundFlow.created_at.desc())

        if sql_res is not None:
            date_start = input_json.get("date_start", "")
            date_end = input_json.get("date_end", "")
            if date_start and date_end:
                sql_res = sql_res\
                    .where(FundFlow.created_at.between(date_start, date_end))\
                    .group_by(SQL('date'))
            else:
                sql_res = sql_res.group_by(SQL('date'))

            total_num =  len(sql_res)
            page_number = input_json.get("page_number", 1)
            length = input_json.get("length", 20)
            sql_res = sql_res.paginate(page_number, length)
            fund_flows = sql_res.dicts()

            datas = []
            for fund_flow in fund_flows:
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
            res.Result = {
                "data":datas,
                "total":total_num
            }
        else:
            res.Code = 401
            res.Message = "no have permission"
        return jsonify(res.object_to_dict())
    except:
        res.Code = 500
        res.Message = "Interval Error"
        return jsonify(res.object_to_dict())

