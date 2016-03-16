import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'df32tgi32(=vfT2G!'
    DEBUG = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = ""

    @classmethod
    def init_app(cls, app):
        print "init app..."

        if os.getenv('SERVER_SOFTWARE') \
                and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/'):
            # deploy data base URI
            cls.SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@127.0.0.1:3306/hwCheck-db' \
                                          '?unix_socket=/cloudsql/hwcheck-1224:hwcheck?charset=utf8'
        else:
            print "local!!!!"
            # dev_appserver.py or appengine launcher
            cls.SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost/hwCheck-db'
            # cls.SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:12341234@173.194.242.35/hwCheck-db'

        app.config.from_object(cls)
