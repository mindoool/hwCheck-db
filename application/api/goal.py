from . import api
from application.model.goal import Goal


@api.route("/")
def test():
    return "hello"