# -*- coding: utf-8 -*-
from application import db
from application.models.homework import Homework
from application.models.group import Group
from application.models.user import User
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class Problem(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))
    homework = db.relationship('Homework', foreign_keys=[homework_id])
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User', foreign_keys=[user_id])

    @classmethod
    def get_query(cls, filter_condition=None):
        q = db.session.query(cls, Homework)

        if filter_condition is not None:
            q = q.filter(filter_condition)

        return q.outerjoin(Homework, Homework.id == cls.homework_id)
