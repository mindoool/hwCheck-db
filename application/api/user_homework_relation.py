# -*- coding: utf-8 -*-
from flask import request, jsonify
from . import api
from application import db
from application.models.user_homework_relation import UserHomeworkRelation
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.rest.auth_helper import required_admin


# read
@api.route('/user-homework-relations/<int:user_homework_relation_id>', methods=['GET'])
# @required_token
def get_user_homework_relation_by_id(user_homework_relation_id):
    try:
        user_homework_relation = UserHomeworkRelation.get_query(
            filter_condition=(UserHomeworkRelation.id == user_homework_relation_id))
        return jsonify(
            data=SerializableModelMixin.serialize_row(user_homework_relation.one())
        ), 200

    except:
        return jsonify(
            userMessage="해당 관계를 찾을 수 없습니다."
        ), 404


# read
@api.route('/user-homework-relations', methods=['GET'])
# @required_token
def get_user_homework_relations():
    if request.args.get('userId') is not None:
        user_id = int(request.args.get('userId'))
    else:
        user_id = 0

    if request.args.get('homeworkId'):
        homework_id = int(request.args.get('homeworkId'))
    else:
        homework_id = 0

    if user_id >= 1 and homework_id >= 1:
        filter_condition = (UserHomeworkRelation.user_id == user_id, UserHomeworkRelation.homework_id == homework_id)

    elif user_id >= 1 >= homework_id:
        filter_condition = (UserHomeworkRelation.user_id == user_id)
    elif homework_id >= 1 >= user_id:
        filter_condition = (UserHomeworkRelation.homework_id == homework_id)
    else:
        filter_condition = None
    # filter_condition = None

    print filter_condition

    user_homework_relations = UserHomeworkRelation.get_query(filter_condition=filter_condition)

    return jsonify(
        data=map(SerializableModelMixin.serialize_row, user_homework_relations)
    ), 200


# update
@api.route('/user-homework-relations/<int:user_homework_relation_id>', methods=['PUT'])
# @required_admin
def update_user_homework_relation(user_homework_relation_id):
    request_params = request.get_json()
    user_id = request_params.get('userId')
    homework_id = request_params.get('homeworkId')
    try:
        user_homework_relation = db.session.query(UserHomeworkRelation).get(user_homework_relation_id)

        if user_id is not None and user_homework_relation.user_id != user_id:
            user_homework_relation.user_id = user_id

        if homework_id is not None and user_homework_relation.homework_id != homework_id:
            user_homework_relation.homework_id = homework_id

        db.session.commit()

        return jsonify(
            data=user_homework_relation.serialize()
        ), 201

    except:
        return jsonify(
            userMessage="해당 관계를 찾을 수 없습니다."
        ), 404


# delete
@api.route('/user-homework-relations/<int:user_homework_relation_id>', methods=['DELETE'])
# @required_admin
def delete_user_homework_relation(user_homework_relation_id):
    try:
        user_homework_relation = db.session.query(UserHomeworkRelation).get(user_homework_relation_id)

        try:
            db.session.delete(user_homework_relation)
            return jsonify(
                userMessage="삭제가 완료되었습니다."
            ), 200
        except:
            return jsonify(
                userMessage="server error, try again"
            ), 403

    except:
        return jsonify(
            userMessage="해당 관계를 찾을 수 없습니다."
        ), 404
