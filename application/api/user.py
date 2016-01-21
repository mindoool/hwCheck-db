# -*- coding: utf-8 -*-
from flask import request, jsonify, abort
from . import api
from application import db
from application.models.user import User
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.encript.encript_helper import password_encode


# login
@api.route('/users/login', methods=['POST'])
def login():
    request_params = request.get_json()
    email = request_params.get('email')
    password = request_params.get('password')

    # TODO  regex, password validation need
    if email is None:
        return jsonify(
            userMessage="required field: email"
        ), 400

    if password is None:
        return jsonify(
            userMessage="required field: password"
        ), 400

    encoded_password = password_encode(password)
    q = db.session.query(User) \
        .filter(User.email == email,
                User.password == encoded_password
                )
    user = q.first()

    if user is None:
        return jsonify(
            userMessage="invalid password/email"
        ), 404

    token = user.get_token()
    user_data = user.serialize()
    return jsonify(
        data=user_data,
        token=token
    ), 200


# create
@api.route('/users', methods=['POST'])
def sign_up():
    request_params = request.get_json()
    email = request_params.get('email')
    password = request_params.get('password')

    # TODO  regex, password validation need
    if email is None:
        return jsonify(
            userMessage="이메일 입력을 확인해주세요."
        ), 400

    if password is None:
        return jsonify(
            userMessage="비밀번호 입력을 확인해주세요."
        ), 400

    q = db.session.query(User) \
        .filter(User.email == email)

    if q.count() > 0:
        return jsonify(
            userMeesage="already enrolled email"
        ), 409

    user = User.add(request_params)

    if user is None:
        return jsonify(
            userMessage="server error, try again"
        ), 400

    token = user.get_token()
    user_data = user.serialize()

    return jsonify(
        data=user_data,
        token=token
    ), 201


# read
@api.route('/users/<int:user_id>', methods=['GET'])
@required_token
def get_user_by_id(user_id):
    user = db.session.query(User).get(user_id)

    if user is None:
        return jsonify(
            userMessage="can not find user"
        ), 404

    user_data = user.serialize()
    return jsonify(
        data=user_data
    ), 200


# read
@api.route('/users', methods=['GET'])
@required_token
def users():
    limit = request.args.get('limit', 10)
    last_id = request.args.get('lastId')
    q = db.session.query(User)

    if last_id is not None:
        q = q.filter(User.id < last_id)

    q = q.order_by(User.id.desc()).limit(limit)
    return_data = map(SerializableModelMixin.serialize_row, q.all())

    return jsonify(
        data=return_data
    ), 200


# update
@api.route('/users/<int:user_id>', methods=['PUT'])
@required_token
def update_user(user_id, request_user_id=None):   # request_user_id 형식은 어디서 가져오는지?
    try:
        request_user = db.session.query(User).get(request_user_id)
    except:
        return jsonify(
            userMessage="수정 요청을 보낸 유저를 찾을 수 없습니다."
        ), 404

    if not (user_id == request_user.id):
        return jsonify(
            userMessage="해당 정보를 바꿀 권한이 없습니다."
        ), 401

    try:
        user = db.session.query(User).get(user_id)
    except:
        return jsonify(
            userMessage="해당 유저를 찾을 수 없습니다."
        ), 404

    request_params = request.get_json()
    password = request_params.get('password')

    if password is not None:
        user.password = password

    db.session.commit()
    user_data = user.serialize()

    return jsonify(
        data=user_data
    ), 200


# delete
@api.route('/users/<int:user_id>', methods=['DELETE'])
@required_token
def delete_user(request_user_id=None):
    try:
        user = db.session.query(User).get(request_user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify(
                userMessage="delete done"
            ), 200
        except:
            return jsonify(
                userMessage="server error, try again"
            ), 403

    except:
        return jsonify(
            userMessage="can not find user"
        ), 404