# -*- coding:utf-8 -*-
import os
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from utils.flask_json_encode import JSONEncoder
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from configuration import config_obj
from flask_config import config


class RetryMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass
    # def begin(self):
    #     # db api 并没有自动加 begin 语句，所以在此要手动加上
    #     self.get_conn().begin()


db = RetryMySQLDatabase(
    config_obj.get('db', 'database'),
    max_connections=config_obj.getint('db', 'max_connections'),
    stale_timeout=config_obj.getint('db', 'stale_timeout'),
    host=config_obj.get('db', 'host'),
    user=config_obj.get('db', 'user'),
    password=config_obj.get('db', 'password'),
    port=config_obj.getint('db', "port")
)

from playhouse.flask_utils import FlaskDB


def create_app(config_name):
    _app = Flask(__name__)
    _app.config.from_object(config[config_name])
    _app.json_encoder = JSONEncoder
    config[config_name].init_app(_app)
    CORS(_app, supports_credentials=True)
    FlaskDB(_app, db)
    from .admin_server import admin_server
    _app.register_blueprint(admin_server, url_prefix='/admin_server/v1')

    from .app2 import app2
    _app.register_blueprint(app2, url_prefix='/app2/v1')

    if config[config_name].swagger_config.get("template"):
        swagger = Swagger(_app, config=config[config_name].swagger_config,
                          template=config[config_name].swagger_config.get("template"))
    else:
        swagger = Swagger(_app, config=config[config_name].swagger_config)
    return _app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
from . import views
