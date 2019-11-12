# -*- coding:utf-8 -*-
import datetime
from peewee import (
    DateTimeField,
    Model,
    SQL,
    DateField,
    IntegerField,
    CharField
)

from apps import db


class ModelBase(Model):
    created_at = DateTimeField(default=datetime.datetime.now, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(default=datetime.datetime.now, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP'),
                                                                           SQL('ON UPDATE CURRENT_TIMESTAMP')])

    def update_dict(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    class Meta:
        database = db
        only_save_dirty = True
