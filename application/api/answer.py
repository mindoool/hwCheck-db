# -*- coding: utf-8 -*-
from flask import request, jsonify
from . import api
from application import db
from application.models.answer import Answer
from application.models.problem import Problem
from application.models.user_homework_relation import UserHomeworkRelation
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.rest.auth_helper import required_admin


# create
@api.route('/answers', methods=['POST'])
@required_token
def create_answers(request_user_id=None):
    request_params = request.get_json()
    problem_answer_list = request_params.get('problemAnswers')
    homework_id = request_params.get('homeworkId')

    # TODO  regex, password validation need
    if problem_answer_list is None:
        return jsonify(
            userMessage="입력된 답이 없습니다."
        ), 400

    # 답 한번에 add할 때 사용할 리스트
    answer_list = []

    for problem_answer in problem_answer_list:
        print problem_answer
        if problem_answer["answer"] == "":
            return jsonify(
                userMessage="답안 입력이 안됐습니다."
            ), 400

        q = db.session.query(Answer).filter(Answer.problem_id == problem_answer["id"],
                                            Answer.user_id == request_user_id)
        if q.count() > 0:
            return jsonify(
                userMeesage="이미 등록된 답입니다."
            ), 409

        try:
            answer = Answer(problem_id=problem_answer['id'], user_id=request_user_id,
                            content=problem_answer['answer']['content'].strip())
            answer_list.append(answer)
        except:
            return jsonify(
                userMessage="답안 등록에 실패하였습니다."
            )

    db.session.add_all(answer_list)

    user_homework = db.session.query(UserHomeworkRelation).filter(UserHomeworkRelation.user_id == request_user_id,
                                                                  UserHomeworkRelation.homework_id == homework_id).first()
    if user_homework is None:
        return jsonify(
            userMessage="해당 숙제가 맞는지 확인해 보세요."
        )

    user_homework.is_submitted = True

    db.session.commit()

    return jsonify(
        data=[answer.serialize() for answer in answer_list]
    ), 201


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

    if request.args.get('homeworkId'):
        homework_id = int(request.args.get('homeworkId'))
        problems = db.session.query(Problem).filter(Problem.homework_id == homework_id).order_by(Problem.id)
    else:
        homework_id = 0
        problems = db.session.query(Problem).order_by(Problem.id)

    if user_id >= 1 and homework_id >= 1:
        filter_condition = (Answer.user_id == user_id, Problem.homework_id == homework_id)

    elif user_id >= 1 >= homework_id:
        filter_condition = (Answer.user_id == user_id)
    elif homework_id >= 1 >= user_id:
        filter_condition = (Problem.homework_id == homework_id)
    else:
        filter_condition = None

    answers = Answer.get_query(filter_condition=filter_condition).order_by(Answer.user_id, Answer.problem_id)

    prev_user_id = None
    prev_problem_id = None
    return_object = {}
    answer_object = {}
    for row in answers:
        print "a"
        (answer, user, problem, homework) = row
        if prev_user_id != user.id:
            return_object[user.name] = []
            prev_user_id = user.id
            print "b"
        return_object[user.name].append(SerializableModelMixin.serialize_row(row))

    # 문제 목록 쫙 호출하기
    return_object['problems'] = map(lambda x: x.serialize(), problems)

    return jsonify(
        # data=map(SerializableModelMixin.serialize_row, answer)
        data=return_object
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
