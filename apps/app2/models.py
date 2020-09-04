# -*- coding:utf-8 -*-
from datetime import datetime
from apps import db


# ------------------------------------------------models--------------------------------------------------


class Base(db.Model):
    __tablename__ = 'base'
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
