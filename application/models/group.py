# -*- coding: utf-8 -*-
from application import db
from application.models.course import Course
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class Group(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', foreign_keys=[course_id])

    @classmethod
    def get_query(cls, filter_condition=None):
        q = db.session.query(cls, Course)

        if filter_condition is not None:
            q = q.filter(filter_condition)

        return q.join(Course, Course.id == cls.course_id)
