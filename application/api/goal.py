from . import api
from application.models.goal import Goal


@api.route("/")
def test():
    return "hello"