# -*- coding: utf-8 -*-
from application import db
from application.models.user import User
from application.models.problem import Problem
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class Answer(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id])
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
    problem = db.relationship('Problem', foreign_keys=[problem_id])

    @classmethod
    def get_query(cls, filter_condition=None):
        q = db.session.query(cls, User, Problem)

        if filter_condition is not None:
            q = q.filter(filter_condition)

        return q.join(User, User.id == cls.user_id) \
            .join(Problem, Problem.id == cls.problem_id)
