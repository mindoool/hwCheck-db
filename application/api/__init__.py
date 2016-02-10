from flask import Blueprint

api = Blueprint('api', __name__)

from . import (
    course,
    group,
    homework,
    problem,
    user,
    user_group_relation,
    answer
)
