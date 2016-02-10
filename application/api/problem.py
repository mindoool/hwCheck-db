# -*- coding: utf-8 -*-
import datetime
from flask import request, jsonify, abort
from . import api
from application import db
from application.models.problem import Problem
from application.models.group import Group
from application.models.homework import Homework
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.rest.auth_helper import required_admin


# create
@api.route('/problems', methods=['POST'])
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

    try:
        for i in range(number):
            group_id = db.session.query(Group).filter(Group.name == content[i]['data'][0]).first().id
            homework_name = content[i]['data'][1]
            date = content[i]['data'][2].split('-')
            date_object = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            problem_name = content[i]['data'][3]

            # 숙제가 없는 경우 만들어주기 - name, date, group_id
            q = db.session.query(Homework).filter(Homework.name == homework_name)
            if q is not None:
                homework_id = q.first().id
            else:
                homework = Homework(name=homework_name, date=date_object, group_id=group_id)
                db.session.add(homework)
                db.session.commit()
                homework_id = homework.id

            # 이미 동일한 문제가 있을 경우 아무짓도 안하도록
            problem = db.session.query(Problem).filter(Problem.group_id == group_id, Problem.name == problem_name,
                                                       Problem.date == date_object).first()
            # 문제 만들기 - name, homework_id
            if problem is None:
                problem = Problem(name=problem_name, homework_id=homework_id)
                problem_list.append(problem)

        db.session.add_all(problem_list)
        db.session.commit()

        return jsonify(
            data=[problem.serialize() for problem in problem_list]
        ), 201
    except:
        return jsonify(
            userMessage="문제 등록에 실패하였습니다."
        ), 403


# read
@api.route('/homeworks/<int:homework_id>/problems/<int:problem_id>', methods=['GET'])
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
# @required_token
def get_problems(homework_id):
    group_id = request.args.get('groupId', 0)

    if group_id != 0:
        filter_condition = (Problem.homework_id == homework_id)
    else:
        filter_condition = None

    # group_id 가지고도 filter condition 넣는게 필요하지 않을까...

    q = Problem.get_query(filter_condition=filter_condition)

    # start date end date 처리
    if request.args.get('date1') is None:
        date1 = datetime.date.today()
        print request.args.get('date')
    else:
        date1 = datetime.datetime.strptime(request.args.get('date1'), "%Y-%m-%d")
        print request.args.get('date1')

    if request.args.get('date2') is None:
        date2 = datetime.date.today()
        print request.args.get('date')
    else:
        date2 = datetime.datetime.strptime(request.args.get('date2'), "%Y-%m-%d")
        print request.args.get('date2')

    q = q.filter(Problem.date.between(date1, date2))

    # if request.args.get('group') is not None:
    #     if request.args.get('group') =="":
    #         pass
    #     else:
    #         group_id = db.session.query(Group).filter(Group.name == request.args.get('group')).one().id
    #         q = q.filter(Problem.group_id == group_id)

    return jsonify(
        data=map(SerializableModelMixin.serialize_row, q)
    ), 200


# update
@api.route('/homeworks/<int:homework_id>/problems/<int:problem_id>', methods=['PUT'])
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
