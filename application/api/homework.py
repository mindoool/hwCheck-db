# -*- coding: utf-8 -*-
from flask import request, jsonify, abort
from . import api
from application import db
from application.models.homework import Homework
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.rest.auth_helper import required_admin


# create - problem 만들 때 homework 만들거얌..


# read
@api.route('/groups/<int:group_id>/homeworks/<int:homework_id>', methods=['GET'])
# @required_token
def get_homework_by_id(group_id, homework_id):
    try:
        homework = Homework.get_query(filter_condition=(Homework.id == homework_id))
        return jsonify(
            data=SerializableModelMixin.serialize_row(homework.one())
        ), 200

    except:
        return jsonify(
            userMessage="해당 숙제를 찾을 수 없습니다."
        ), 404


# read
@api.route('/groups/<int:group_id>/homeworks', methods=['GET'])
# @required_token
def get_homeworks(group_id=0):
    if group_id != 0:
        filter_condition = (Homework.group_id == group_id)
    else:
        filter_condition = None

    homeworks = Homework.get_query(filter_condition=filter_condition)

    return jsonify(
        data=map(SerializableModelMixin.serialize_row, homeworks)
    ), 200


# update
@api.route('/groups/<int:group_id>/homeworks/<int:homework_id>', methods=['PUT'])
# @required_admin
def update_homework(group_id, homework_id):
    request_params = request.get_json()
    name = request_params.get('name')
    new_group_id = request_params.get('groupId')
    try:
        homework = db.session.query(Homework).get(homework_id)

        if name is not None and homework.name != name:
            homework.name = name

        if new_group_id is not None and new_group_id != group_id:
            homework.group_id = new_group_id

        db.session.commit()

        return jsonify(
            data=homework.serialize()
        ), 201

    except:
        return jsonify(
            userMessage="해당 반을 찾을 수 없습니다."
        ), 404


# delete
@api.route('/groups/<int:group_id>/homeworks/<int:homework_id>', methods=['DELETE'])
# @required_admin
def delete_homework(group_id, homework_id):
    try:
        homework = db.session.query(Homework).get(homework_id)

        try:
            db.session.delete(homework)
            return jsonify(
                userMessage="삭제가 완료되었습니다."
            ), 200
        except:
            return jsonify(
                userMessage="server error, try again"
            ), 403

    except:
        return jsonify(
            userMessage="해당 반을 찾을 수 없습니다."
        ), 404
