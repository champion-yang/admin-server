from flask import Blueprint


app2 = Blueprint('app2', __name__)

from . import view_demo2
