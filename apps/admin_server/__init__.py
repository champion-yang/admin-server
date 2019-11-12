from flask import Blueprint


admin_server = Blueprint('admin_server', __name__)

from . import auth, data_analusis, account_manage
