# -*- coding:utf-8 -*-
import os
from configuration import config_obj
from flasgger import Swagger

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    # SQLALCHEMY_ECHO = True
    JSON_AS_ASCII = False
    swagger_config = Swagger.DEFAULT_CONFIG
    swagger_config['openapi'] = "3.0.2"
    swagger_config['title'] = "xxx API"  # 配置大标题
    swagger_config['version'] = "1.0.0"  # 配置版本
    swagger_config['termsOfService'] = ""  # 配置大标题
    swagger_config['description'] = ""  # 配置公共描述内容
    swagger_config['template'] = {
        "swagger": "3.0.2",
        "info": {
            "title": "xxx API",
            "description": "xxx System",
            "version": "1.0.0"
        },
        "basePath": "/",  # base bash for blueprint registration
        "schemes": [
            "http",
            # "https"
        ],
        "operationId": "getmyData"
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    JSON_AS_ASCII = False


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    JSON_AS_ASCII = False
    swagger_config = Swagger.DEFAULT_CONFIG


config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}
