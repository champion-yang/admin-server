# -*- coding:utf-8 -*-
from apps import db
from peewee import (DateTimeField, CharField,
                    IntegerField, SmallIntegerField,
                    DecimalField, TextField,
                    DateField, BigIntegerField, Model, SQL
                    )
from apps.base_models import ModelBase
from datetime import datetime, timedelta
import jwt
import logging
from configuration import config_obj
import datetime

class Account(ModelBase):
    id = IntegerField(primary_key=True)
    name = CharField()
    remark = CharField()
    org = CharField()
    consumer_id = CharField()
    status = IntegerField()
    amount = DecimalField()
    allow_credit = DecimalField()
    alert_threshold = DecimalField()
    pricing_id = IntegerField()

    class Meta:
        database = db
        table_name = 'account'

# fund_flow mysql中没有update_at 插入可能会报错
class FundFlow(Model):
    id = IntegerField(primary_key=True)
    account_id = IntegerField()
    fund_type = IntegerField()
    fund_detail = TextField()
    amount = DecimalField()
    remain_amount = DecimalField()
    pricing_id = IntegerField()
    request_id = CharField()
    created_at = DateTimeField(default=datetime.datetime.now, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = db
        table_name = 'fund_flow'

class FundType(ModelBase):
    fund_type = IntegerField(primary_key=True)
    name = CharField()

    class Meta:
        database = db
        table_name = 'fund_type'

class Organization(ModelBase):
    code = CharField()
    name = CharField()
    type = CharField()
    tags = CharField()

    class Meta:
        database = db
        table_name = 'organization'

class Pricing(ModelBase):
    id = IntegerField(primary_key=True)
    account_id = IntegerField()
    active_time = DateField()
    deactive_time = DateField()
    currency = CharField()
    pricing_config = TextField()

    class Meta:
        database = db
        table_name = 'pricing'

class RequestAggr(ModelBase):
    id = IntegerField(primary_key=True)
    date = DateField()
    org = CharField()
    path = CharField()
    param1 = CharField()
    param2 = CharField()
    param3 = CharField()
    first_req_id = BigIntegerField()
    account_id = IntegerField()
    active_time = DateField()
    deactive_time = DateField()
    fund_typecurrency = CharField()
    pricing_config = TextField()

    class Meta:
        database = db
        table_name = 'request_aggr'

class RequestLog(ModelBase):
    id = IntegerField(primary_key=True)
    request_id = CharField()
    account_id = IntegerField()
    key_id = CharField()
    org = CharField()
    endpoint = CharField()
    method = CharField()
    path = CharField()
    body = TextField()
    ip = CharField()
    ua = CharField()
    response_status = SmallIntegerField()
    response_body = TextField()

    class Meta:
        database = db
        table_name = 'request_log'

class User(ModelBase):
    id = IntegerField(primary_key=True)
    user_name = CharField()
    password = CharField()
    role_id = IntegerField()
    account_id = IntegerField()
    last_login_at = DateTimeField()
    status = SmallIntegerField()

    class Meta:
        database = db
        table_name = 'user'

