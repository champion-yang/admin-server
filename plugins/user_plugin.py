import jwt
import logging
from configuration import config_obj
from flask import request, abort
from datetime import datetime, timedelta


def encode_auth_token(user_id, account_id):
    """
    生成认证Token
    :return: string
    """
    try:
        # token七天过期，需要重新登录 测试1天过期
        expire_at = datetime.now() + timedelta(1)
        payload = {
            "user_id": user_id,
            "account_id": account_id,
            "login_time": (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
            "exp": expire_at
        }
        jwt_en = jwt.encode(
            payload,
            config_obj.get('user', 'secret'),
            algorithm="HS256"
        ).decode('utf-8')
        return jwt_en
    except Exception as e:
        logging.info("create authentication error %s %s", user_id, e)
        return e

def get_jwt_user():
    """
    解密token，得到payload
    :return:
    """
    secret = config_obj.get("user", "secret")
    algorithms = config_obj.get("user", "algorithms")
    try:
        token = request.headers['Authorization']
        payload =  jwt.decode(token, secret, algorithms=algorithms)
        if payload and 'user_id' in payload:
            return payload
    except:
        abort(401, "Invalid JWT header")



