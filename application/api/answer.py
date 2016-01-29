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