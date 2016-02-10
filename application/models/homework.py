# -*- coding: utf-8 -*-
from application import db
from application.models.course import Course
from application.models.group import Group
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class Homework(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.Date, default=db.func.current_timestamp())
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', foreign_keys=[group_id])

    @classmethod
    def get_query(cls, filter_condition=None):
        q = db.session.query(cls, Group, Course)

        if filter_condition is not None:
            q = q.filter(filter_condition)

        return q.outerjoin(Group, Group.id == cls.group_id)\
            .outerjoin(Course, Course.id == Group.course_id)