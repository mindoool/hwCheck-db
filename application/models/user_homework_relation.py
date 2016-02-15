# -*- coding: utf-8 -*-
from application import db
from application.models.user import User
from application.models.group import Group
from application.models.homework import Homework
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class UserHomeworkRelation(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id])
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))
    homework = db.relationship('Homework', foreign_keys=[homework_id])
    is_submitted = db.Column(db.Boolean, default=False)

    @classmethod
    def get_query(cls, filter_condition=None):
        q = db.session.query(Homework, cls, Group)

        if filter_condition is not None:
            q = q.filter(filter_condition)

        return q.outerjoin(cls, cls.homework_id == Homework.id) \
            .outerjoin(Group, Group.id == Homework.group_id) \
            .order_by(cls.is_submitted, Homework.date, Group.id)
