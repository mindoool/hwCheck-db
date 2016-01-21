# -*- coding: utf-8 -*-
from application import db
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class Homework(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.Date, default=db.func.current_timestamp())
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course',
                             foreign_keys=[course_id])
    is_completed = db.Column(db.Boolean, default=False)
    completed_time = db.Column(db.DateTime, default=db.func.current_timestamp())
