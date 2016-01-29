# -*- coding: utf-8 -*-
from flask import request, jsonify
from . import api
from application import db
from application.models.user_group_relation import UserGroupRelation
from application.models.user import User
from application.models.group import Group
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.rest.auth_helper import required_admin


# read
@api.route('/user-group-relations/<int:user_group_relation_id>', methods=['GET'])
# @required_token
def get_user_group_relation_by_id(user_group_relation_id):
    try:
        user_group_relation = UserGroupRelation.get_query(
            filter_condition=(UserGroupRelation.id == user_group_relation_id))
        return jsonify(
            data=SerializableModelMixin.serialize_row(user_group_relation.one())
        ), 200

    except:
        return jsonify(
            userMessage="해당 관계를 찾을 수 없습니다."
        ), 404


# read
@api.route('/user-group-relations', methods=['GET'])
# @required_token
def get_user_group_relations():
    if request.args.get('userId') is not None:
        user_id = int(request.args.get('userId'))
    else:
        user_id = 0

    if request.args.get('userId'):
        group_id = int(request.args.get('groupId'))
    else:
        group_id = 0

    print user_id
    print group_id

    if user_id >= 1 and group_id >= 1:
        filter_condition = (UserGroupRelation.user_id == user_id, UserGroupRelation.group_id == group_id)

    elif user_id >= 1 >= group_id:
        filter_condition = (UserGroupRelation.user_id == user_id)
    elif group_id >= 1 >= user_id:
        filter_condition = (UserGroupRelation.group_id == group_id)
    else:
        filter_condition = None
    # filter_condition = None

    print filter_condition

    user_group_relations = UserGroupRelation.get_query(filter_condition=filter_condition)

    return jsonify(
        data=map(SerializableModelMixin.serialize_row, user_group_relations)
    ), 200


# update
@api.route('/user-group-relations/<int:user_group_relation_id>', methods=['PUT'])
# @required_admin
def update_user_group_relation(user_group_relation_id):
    request_params = request.get_json()
    user_id = request_params.get('userId')
    group_id = request_params.get('groupId')
    try:
        user_group_relation = db.session.query(UserGroupRelation).get(user_group_relation_id)

        if user_id is not None and user_group_relation.user_id != user_id:
            user_group_relation.user_id = user_id

        if group_id is not None and user_group_relation.group_id != group_id:
            user_group_relation.group_id = group_id

        db.session.commit()

        return jsonify(
            data=user_group_relation.serialize()
        ), 201

    except:
        return jsonify(
            userMessage="해당 관계를 찾을 수 없습니다."
        ), 404


# delete
@api.route('/user-group-relations/<int:user_group_relation_id>', methods=['DELETE'])
# @required_admin
def delete_user_group_relation(user_group_relation_id):
    try:
        user_group_relation = db.session.query(UserGroupRelation).get(user_group_relation_id)

        try:
            db.session.delete(user_group_relation)
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
