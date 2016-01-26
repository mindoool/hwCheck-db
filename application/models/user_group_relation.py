# -*- coding: utf-8 -*-
from application import db
from application.models.user import User
from application.models.group import Group
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class UserGroupRelation(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id])
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', foreign_keys=[group_id])

    @classmethod
    def get_query(cls, filter_condition=None):
        q = db.session.query(cls, User, Group)

        if filter_condition is not None:
            q = q.filter(filter_condition)

        return q.join(User, User.id == cls.user_id) \
            .join(Group, Group.id == cls.group_id)
