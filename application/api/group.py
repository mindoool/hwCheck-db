# -*- coding: utf-8 -*-
from flask import request, jsonify, abort
from . import api
from application import db
from application.models.group import Group
from application.models.course import Course
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.rest.auth_helper import required_admin


# create name, course_id
@api.route('/courses/<int:course_id>/groups', methods=['POST'])
@required_admin
def create_groups(course_id):
    name = request.get_json().get('name')

    # TODO  regex, password validation need
    if name is None:
        return jsonify(
            userMessage="반명을 입력해주세요."
        ), 400

    q = db.session.query(Group).filter(Group.name == name, Group.course_id == course_id)

    if q.count() > 0:
        return jsonify(
            userMeesage="이미 등록된 그룹입니다."
        ), 409

    try:
        group = Group(name=name, course_id=course_id)

        db.session.add(group)
        db.session.commit()

        return jsonify(
            data=group.serialize()
        ), 200
    except:
        return jsonify(
            userMessage="반 생성에 실패하였습니다."
        ), 403


# read
@api.route('/courses/<int:course_id>/groups/<int:group_id>', methods=['GET'])
@required_token
def get_group_by_id(course_id, group_id):
    try:
        group = Group.get_query(filter_condition=(Group.id == group_id))
        return jsonify(
            data=SerializableModelMixin.serialize_row(group.one())
        ), 200

    except:
        return jsonify(
            userMessage="해당 반을 찾을 수 없습니다."
        ), 404


# read
@api.route('/courses/<int:course_id>/groups', methods=['GET'])
@required_token
def get_groups(course_id=0):
    if course_id != 0:
        filter_condition = (Group.course_id == course_id)
    else:
        filter_condition = None

    group = Group.get_query(filter_condition=filter_condition)

    return jsonify(
        data=map(SerializableModelMixin.serialize_row, group)
    ), 200


# update
@api.route('/courses/<int:course_id>/groups/<int:group_id>', methods=['PUT'])
@required_admin
def update_group(course_id, group_id):
    request_params = request.get_json()
    name = request_params.get('name')
    new_course_id = request_params.get('courseId')
    try:
        group = db.session.query(Group).get(group_id)

        if name is not None and group.name != name:
            group.name = name

        if new_course_id is not None and new_course_id != course_id:
            group.course_id = new_course_id

        db.session.commit()

        return jsonify(
            data=group.serialize()
        ), 201

    except:
        return jsonify(
            userMessage="해당 반을 찾을 수 없습니다."
        ), 404


# delete
@api.route('/courses/<int:course_id>/groups/<int:group_id>', methods=['DELETE'])
@required_admin
def delete_group(course_id, group_id):
    try:
        group = db.session.query(Group).get(group_id)

        try:
            db.session.delete(group)
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
