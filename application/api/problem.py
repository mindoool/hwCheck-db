# -*- coding: utf-8 -*-
import datetime
from flask import request, jsonify, abort
from . import api
from application import db
from application.models.problem import Problem
from application.models.group import Group
from application.models.homework import Homework
from application.models.answer import Answer
from application.models.user_group_relation import UserGroupRelation
from application.models.user_homework_relation import UserHomeworkRelation
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.rest.auth_helper import required_admin


# create
@api.route('/problems', methods=['POST'])
@required_admin
def create_problems():
    request_params = request.get_json()
    content = request_params.get('content')
    headers = content.pop(0)
    number = len(content)

    if content is None:
        return jsonify(
            userMessage="입력된 정보가 없습니다."
        ), 400

    problem_list = []

    # try:
    for i in range(number):
        group_id = db.session.query(Group).filter(Group.name == content[i]['data'][0]).first().id
        homework_name = content[i]['data'][1]
        date = content[i]['data'][2].split('-')
        date_object = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        problem_name = content[i]['data'][3]

        # 숙제가 없는 경우 만들어주기 - name, date, group_id
        q = db.session.query(Homework).filter(Homework.name == homework_name).first()
        if q is not None:
            homework_id = q.id
        else:
            homework = Homework(name=homework_name, date=date_object, group_id=group_id)
            db.session.add(homework)
            db.session.commit()
            homework_id = homework.id
            print homework_id
            # user-homework사이의 관계 추가
            user_group_relations = db.session.query(UserGroupRelation).filter(UserGroupRelation.group_id == group_id)
            print user_group_relations
            print "aa"
            for user_group_relation in user_group_relations:
                print "bb"
                if db.session.query(UserHomeworkRelation).filter(
                                UserHomeworkRelation.user_id == user_group_relation.user_id,
                                UserHomeworkRelation.homework_id == homework_id).first() is None:
                    user_homework_relation = UserHomeworkRelation(user_id=user_group_relation.user_id,
                                                                  homework_id=homework.id)
                    db.session.add(user_homework_relation)
                    print "cc"

        # 이미 동일한 문제가 있을 경우 아무짓도 안하도록
        problem = db.session.query(Problem).filter(Problem.homework_id == homework_id,
                                                   Problem.name == problem_name).first()
        # 문제 만들기 - name, homework_id
        if problem is None:
            problem = Problem(name=problem_name, homework_id=homework_id)
            problem_list.append(problem)

    db.session.add_all(problem_list)
    db.session.commit()

    return jsonify(
        data=[problem.serialize() for problem in problem_list]
    ), 201
    # except:
    #     return jsonify(
    #         userMessage="문제 등록에 실패하였습니다."
    #     ), 403


# read
@api.route('/homeworks/<int:homework_id>/problems/<int:problem_id>', methods=['GET'])
@required_token
def get_problem_by_id(homework_id, problem_id):
    # try:
    q = Problem.get_query(filter_condition=(Problem.id == problem_id))
    return jsonify(
        data=SerializableModelMixin.serialize_row(q)
    ), 200

    # except:
    #     return jsonify(
    #         userMessage="해당 문제를 찾을 수 없습니다."
    #     ), 404


# read
@api.route('/homeworks/<int:homework_id>/problems', methods=['GET'])
@required_token
def get_problems(homework_id=0, request_user_id=None):
    group_id = request.args.get('groupId', 0)

    if homework_id != 0:
        filter_condition = (Problem.homework_id == homework_id)
    else:
        filter_condition = None

    # group_id 가지고도 filter condition 넣는게 필요하지 않을까...

    q = db.session.query(Problem, Answer).outerjoin(Answer,
                                                    (Answer.problem_id == Problem.id) & (
                                                        Answer.user_id == request_user_id)).filter(filter_condition)
    return jsonify(
        data=map(SerializableModelMixin.serialize_row, q)
    ), 200


# update
@api.route('/homeworks/<int:homework_id>/problems/<int:problem_id>', methods=['PUT'])
@required_admin
def update_problems(homework_id, problem_id):
    request_params = request.get_json()
    name = request_params.get('name')
    new_homework_id = request_params.get('homeworkId')
    try:
        problem = db.session.query(Problem).filter(Problem.id == problem_id, Problem.homework_id == homework_id)

        if name is not None and problem.name != name:
            problem.name = name

        if new_homework_id is not None and problem.group_id != new_homework_id:
            problem.group_id = new_homework_id

        db.session.commit()

        return jsonify(
            data=problem.serialize()
        ), 201

    except:
        return jsonify(
            userMessage="해당 문제를 찾을 수 없습니다."
        ), 404


# delete
@api.route('/homeworks/<int:homework_id>/problems/<int:problem_id>', methods=['DELETE'])
@required_admin
def delete_problems(homework_id, problem_id):
    try:
        problem = db.session.query(Problem).filter(Problem.id == problem_id, Problem.homework_id == homework_id)

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
