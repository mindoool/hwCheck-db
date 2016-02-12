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
    homework = db.relationship('Group', foreign_keys=[homework_id])
    is_submitted = db.Column(db.Boolean, default=False)

    @classmethod
    def get_query(cls, filter_condition=None):
        q = db.session.query(cls, User, Homework, Group)

        if filter_condition is not None:
            q = q.filter(filter_condition)

        return q.join(User, User.id == cls.user_id) \
            .join(Homework, Homework.id == cls.homework_id)\
            .join(Group, Group.id == Homework.group_id)
