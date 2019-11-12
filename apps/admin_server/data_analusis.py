# -*- coding: utf-8 -*-
import os
from flask import jsonify
from flasgger import swag_from
from . import admin_server
from utils.response import Response
from plugins.user_plugin import get_jwt_user
from flask import request
from .models import RequestLog, FundFlow
from peewee import fn, JOIN, SQL
from datetime import datetime

base_dir = os.path.dirname(__file__)
service_yml_path = os.path.join(base_dir, "docs/service_statistic.yml")

@admin_server.route('/service_statistic', endpoint='service_statistic', methods=['POST'])
@swag_from(service_yml_path, endpoint="admin_server.service_statistic", methods=['POST'])
def service_statistic():
    """
    接口次数调用汇总
    :return:
    """
    res = Response()
    get_jwt_user()
    input_json = request.json
    try:
        sql = RequestLog\
            .select(
                RequestLog.path.alias("service"),
                fn.COUNT(RequestLog.id).alias("request_count"),
                fn.SUM(SQL("IF(t2.id IS NOT NULL, 1, 0)")).alias("paid_count")
                )\
            .join(FundFlow, JOIN.LEFT_OUTER, on=(FundFlow.request_id == RequestLog.request_id))
        date_start = input_json.get("date_start", "")
        date_end = input_json.get("date_end", "")
        if input_json and date_start and date_end:
            search_res = sql\
                .where(RequestLog.created_at.between(date_start, date_end))\
                .group_by(RequestLog.path)
        else:
            search_res =  sql.group_by(RequestLog.path)

        res_sql = search_res.dicts()
        res_list = []
        for item in res_sql:
            item["difference_count"] = item["request_count"] - item["paid_count"]
            res_list.append(item)

        request_count = sum([int(k["request_count"]) for k in res_list])
        paid_count = sum([int(k["paid_count"]) for k in res_list])
        difference_count = sum([int(k["difference_count"]) for k in res_list])
        total = {}
        total["request_count"] = request_count
        total["paid_count"] = paid_count
        total["difference_count"] = difference_count

        data = {
            "search_res": res_list,
            "total": total
        }
        res.Code = 200
        res.Message = "success"
        res.Result = data
        return jsonify(res.object_to_dict())

    except Exception as e:
        res.Code = 500
        res.Message = "Internal Server Error"
        return jsonify(res.object_to_dict())
