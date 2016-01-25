# -*- coding: utf-8 -*-
from application import db
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class UserGroupRelation(db.Model, TimeStampMixin, SerializableModelMixin):

    # 기본정보
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200), nullable=False)

    # 추가정보
    course = db.Column(db.String(30))