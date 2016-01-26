# -*- coding: utf-8 -*-
from flask import request, jsonify, abort
from . import api
from application import db
from application.models.course import Course
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token


# create
@api.route('/courses', methods=['POST'])
def create_courses():
    name = request.get_json().get('name')

    # TODO  regex, password validation need
    if name is None:
        return jsonify(
            userMessage="과정명을 입력해주세요."
        ), 400

    q = db.session.query(Course).filter(Course.name == name)

    if q.count() > 0:
        return jsonify(
            userMeesage="이미 등록된 과정입니다."
        ), 409

    try:
        course = Course(name=name)

        db.session.add(course)
        db.session.commit()

        return jsonify(
            data=course.serialize()
        ), 200
    except:
        return jsonify(
            userMessage="과정 등록에 실패하였습니다."
        ), 403


# read
@api.route('/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    try:
        course = db.session.query(Course).get(course_id)
        return jsonify(
            data=course.serialize()
        ), 200

    except:
        return jsonify(
            userMessage="can not find term"
        ), 404


# read
@api.route('/courses', methods=['GET'])
def get_courses():
    q = db.session.query(Course)

    return jsonify(
        data=map(lambda obj: obj.serialize(), q)
    ), 200


# update
@api.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    # try:
    course = db.session.query(Course).get(course_id)

    request_params = request.get_json()
    name = request_params.get('name')
    if name is not None and course.name != name:
        course.name = name

    db.session.commit()

    return jsonify(
        data=course.serialize()
    ), 201

    # except:
    #     return jsonify(
    #         userMessage="과정을 찾을 수 없습니다."
    #     ), 404


# delete
@api.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        course = db.session.query(Course).get(course_id)

        try:
            db.session.delete(course)
            return jsonify(
                userMessage="삭제가 완료되었습니다."
            ), 200
        except:
            return jsonify(
                userMessage="server error, try again"
            ), 403

    except:
        return jsonify(
            userMessage="과정을 찾을 수 없습니다."
        ), 404
