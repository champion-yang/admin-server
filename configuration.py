# -*- coding:utf-8 -*-
import os
import configparser

#  实例化configParser对象
config_obj = configparser.ConfigParser()
# -read读取ini文件
app_env = os.getenv("APP_ENV")
if not app_env:
    app_env = "dev"
config_obj.read('./config/base.ini', encoding='utf-8')
config_obj.read('./config/{}.ini'.format(app_env.lower()), encoding='utf-8')

if __name__ == '__main__':
    # -sections得到所有的section，并以列表的形式返回
    print('sections:', ' ', config_obj.sections())
