# -*- coding: utf-8 -*-
from flask import request, jsonify
from . import api
from application import db
from application.models.answer import Answer
from application.models.user import User
from application.models.problem import Problem
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.rest.auth_helper import required_admin


# create
@api.route('/answers', methods=['POST'])
def create_answers():
    request_params = request.get_json()
    problem_id = request_params.get('problemId')
    user_id = request_params.get('userId')
    content = request_params.get('content')


    # TODO  regex, password validation need
    if content is None:
        return jsonify(
            userMessage="답을 입력해주세요."
        ), 400

    q = db.session.query(Answer).filter(Answer.content == content, Answer.problem_id == problem_id,
                                        Answer.user_id == user_id)

    if q.count() > 0:
        return jsonify(
            userMeesage="이미 등록된 답입니다."
        ), 409

    try:
        for key in request_params.keys():
            request_params[SerializableModelMixin.to_snakecase(key)] = request_params.pop(key)

        answer = Answer(**request_params)

        db.session.add(answer)
        db.session.commit()

        return jsonify(
            data=answer.serialize()
        ), 200
    except:
        return jsonify(
            userMessage="답안 등록에 실패하였습니다."
        ), 403


# read
@api.route('/answers/<int:answer_id>', methods=['GET'])
# @required_token
def get_answer_by_id(answer_id):
    try:
        answer = Answer.get_query(
            filter_condition=(Answer.id == answer_id))
        return jsonify(
            data=SerializableModelMixin.serialize_row(answer.one())
        ), 200

    except:
        return jsonify(
            userMessage="해당 답안을 찾을 수 없습니다."
        ), 404


# read
@api.route('/answers', methods=['GET'])
# @required_token
def get_answers():
    if request.args.get('userId') is not None:
        user_id = int(request.args.get('userId'))
    else:
        user_id = 0

    if request.args.get('problemId'):
        problem_id = int(request.args.get('problemId'))
    else:
        problem_id = 0

    print user_id
    print problem_id

    if user_id >= 1 and problem_id >= 1:
        filter_condition = (Answer.user_id == user_id, Answer.problem_id == problem_id)

    elif user_id >= 1 >= problem_id:
        filter_condition = (Answer.user_id == user_id)
    elif problem_id >= 1 >= user_id:
        filter_condition = (Answer.problem_id == problem_id)
    else:
        filter_condition = None
    # filter_condition = None

    answer = Answer.get_query(filter_condition=filter_condition)

    return jsonify(
        data=map(SerializableModelMixin.serialize_row, answer)
    ), 200


# update
@api.route('/answers/<int:answer_id>', methods=['PUT'])
# @required_admin
def update_answer(answer_id):
    request_params = request.get_json()
    user_id = request_params.get('userId')
    problem_id = request_params.get('problemId')
    content = request_params.get('content')
    try:
        answer = db.session.query(Answer).get(answer_id)

        if user_id is not None and answer.user_id != user_id:
            answer.user_id = user_id

        if problem_id is not None and answer.problem_id != problem_id:
            answer.problem_id = problem_id

        if content is not None and answer.content != content:
            answer.content = content

        db.session.commit()

        return jsonify(
            data=answer.serialize()
        ), 201
    except:
        return jsonify(
            userMessage="해당 답안을 찾을 수 없습니다."
        ), 404


# delete
@api.route('/answers/<int:answer_id>', methods=['DELETE'])
# @required_admin
def delete_answer(answer_id):
    try:
        answer = db.session.query(Answer).get(answer_id)

        try:
            db.session.delete(answer)
            return jsonify(
                userMessage="삭제가 완료되었습니다."
            ), 200
        except:
            return jsonify(
                userMessage="server error, try again"
            ), 403

    except:
        return jsonify(
            userMessage="해당 답안을 찾을 수 없습니다."
        ), 404
