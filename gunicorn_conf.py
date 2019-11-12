# coding:utf-8

from configuration import config_obj

bind = config_obj.get("gunicorn", "bind")
# 64-2048
backlog = config_obj.getint("gunicorn", "backlog")
# workers = multiprocessing.cpu_count() * 3
workers = config_obj.get("gunicorn", "workers")
worker_class = config_obj.get("gunicorn", "worker_class")
# 同步响应最长处理时间
timeout = config_obj.getint("gunicorn", "timeout")
pidfile = config_obj.get("gunicorn", "pidfile")
debug = config_obj.getboolean("gunicorn", "debug")
# gunicorn -c flask_config.py server:application
# 设置日志记录水平
loglevel = 'debug'
# 设置错误信息日志路径
errorlog = '/var/logs/error.logs'
# 设置访问日志路径
accesslog = '/var/logs/access.logs'

# 跑的时候设置log level, 最终就可以将flask的日志输出在gunicorn上了
# $ gunicorn --workers=4 --bind=0.0.0.0:8000 --logs-level=warning apps:apps
