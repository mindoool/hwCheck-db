# -*- coding: utf-8 -*-
from flask import request, jsonify, abort
from . import api
from application import db
from application.models.problem import Problem
from application.models.course import Course
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token


# create
@api.route('/problems', methods=['POST'])
def create_problems():
    request_params = request.get_json()
    content = request_params.get('content')
    number = len(content)

    if content is None:
        return jsonify(
            userMessage="입력된 정보가 없습니다."
        ), 400

    problem_list = []

    try:
        for i in number:
            course_id = db.session.query(Course).filter(Course.name == content[i].course).id

            problem = Problem(name=content[i].name, course_id=course_id, date=content[i].date)
            problem_list.append(problem)

        db.session.add_all(problem_list)
        db.session.commit()

        return jsonify(
            data=problem_list
        ), 201
    except:
        return jsonify(
            userMessage="문제 등록에 실패하였습니다."
        ), 403


# read
@api.route('courses/<int:course_id>/problems/<int:problem_id>', methods=['GET'])
def get_problem_by_id(course_id, problem_id):
    try:
        q = Problem.get_query(filter_condition=(Problem.id == problem_id))
        return jsonify(
            data=SerializableModelMixin.serialize_row(q)
        ), 200

    except:
        return jsonify(
            userMessage="해당 문제를 찾을 수 없습니다."
        ), 404


# read
@api.route('courses/<int:course_id>/problems', methods=['GET'])
def get_problems(course_id):
    q = Problem.get_query(filter_condition=(Problem.course_id == course_id))

    date = request.get_json().get('date')

    if date is not None:
        q = q.filter(Problem.date == date)

    return jsonify(
        data=map(SerializableModelMixin.serialize_row, q.all())
    ), 200


# update
@api.route('courses/<int:course_id>/problems/<int:problem_id>', methods=['PUT'])
def update_problems(course_id, problem_id):
    try:
        problem = db.session.query(Problem).get(problem_id)

        name = request.get_json().get('name')
        if name is not None and problem.name != name:
            problem.name = name

        db.session.commit()

        return jsonify(
            data=problem.serialize()
        ), 201

    except:
        return jsonify(
            userMessage="해당 문제를 찾을 수 없습니다."
        ), 404


# delete
@api.route('courses/<int:course_id>/problems/<int:problem_id>', methods=['DELETE'])
def delete_problems(course_id, problem_id):
    try:
        problem = db.session.query(Problem).get(problem_id)

        try:
            db.session.delete(problem)
            return jsonify(
                userMessage="삭제가 완료되었습니다."
            ), 200
        except:
            return jsonify(
                userMessage="server error, try again"
            ), 403
    except:
        return jsonify(
            userMessage="해당 문제를 찾을 수 없습니다."
        ), 404