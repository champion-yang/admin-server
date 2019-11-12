# -*- coding: utf-8 -*-
import os
from flask import jsonify
from flasgger import swag_from
from . import admin_server
from utils.response import Response
from .models import User
from flask import request
import bcrypt
import logging
from datetime import datetime
from plugins.user_plugin import encode_auth_token, get_jwt_user

base_dir = os.path.dirname(__file__)
login_yml_path = os.path.join(base_dir, "docs/login.yml")
user_yml_path = os.path.join(base_dir, "docs/user.yml")
user_info_yml_path = os.path.join(base_dir, "docs/user_info.yml")

@admin_server.route('/login', endpoint="login", methods=['POST'])
@swag_from(login_yml_path, endpoint="admin_server.login", methods=['POST'])
def login():
    """
    :params: str :user_name
    :params: str :password
    :return:
    """
    input_json = request.json
    res = Response()
    try:
        if input_json and input_json['user_name']:
            user = User.filter(User.user_name == input_json['user_name']).first()
            if not user:
                res.Code = 400
                res.Message = 'username password do not match'
                return jsonify(res.object_to_dict())
            password = input_json['password']
            if isinstance(password, str):
                password = bytes(password, 'utf-8')
            user_password = bytes(user.password, 'utf-8')

            if len(user.password) < 16:
                # 检查是不是 bcrypt 保存的密码 考虑到可能会直接操作数据库进行user信息的写入
                user.password = bcrypt.hashpw(user_password, bcrypt.gensalt())
                is_valid = bcrypt.checkpw(password, user.password)  # 验证成功 true

            else:
                is_valid = bcrypt.checkpw(password, user_password)
            if not is_valid:
                logging.info('%s %s login failed', user.user_name, user.id)
                res.Code = 400
                res.Message = 'username password do not match'
                return jsonify(res.object_to_dict())
            logging.info('%s %s login successed', user.user_name, user.id)
            user.last_login_at = datetime.now()
            user.save()

            res.Code = 200
            res.Message = "login success"
            res.Result = {'jwt': encode_auth_token(user.id, user.account_id)}
            return jsonify(res.object_to_dict())
        else:
            res.Code = 400
            res.Message = "no user name"
            return jsonify(res.object_to_dict())

    except Exception as e:
        res.Code = 500
        res.Message = 'Internal service error %s'%(e)
        return jsonify(res.object_to_dict())

@admin_server.route('/user', endpoint='user', methods=['POST'])
@swag_from(user_yml_path, endpoint="admin_server.user", methods=['POST'])
def user_increase():
    """
    新增用户
    :return:
    """
    input_json = request.json
    if input_json:
        user = User.get_or_none(User.user_name == input_json["user_name"])
        if user:
            logging.info("user already exist %s %s", user.user_name, user.id)
            return {"msg":"user create fail. user already exist"}
        else:
            password = bytes(input_json["password"], "utf-8")
            input_json["password"] = bcrypt.hashpw(password, bcrypt.gensalt())
            User.create(**input_json)
            return {"msg":"user create success"}
    return {"msg":"invalid paramter"}

@admin_server.route('/user', endpoint='user_info', methods=['GET'])
@swag_from(user_info_yml_path, endpoint="admin_server.user_info", methods=['GET'])
def user_info():
    """
    获取用户信息
    :return:
    """
    res = Response()
    payload = get_jwt_user()
    user = User.get_or_none(User.id == payload["user_id"])
    if user:
        user_dict = {
            "id": user.id,
            "created_at": user.created_at,
            "last_login_at": user.last_login_at,
            "role_id": user.role_id,
            "status": user.status,
            "user_name": user.user_name
        }
        res.Code = 200
        res.Message = "success"
        res.Result = user_dict
        return jsonify(res.object_to_dict())
    res.Code = 400
    res.Message = "user not exist"
    return jsonify(res.object_to_dict())
