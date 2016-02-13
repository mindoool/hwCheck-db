# coding: utf8
import re
import datetime
from calendar import timegm
from application import db


class TimeStampMixin(object):
    created_time = db.Column(db.TIMESTAMP,
                             default=db.func.utc_timestamp())
    modified_time = db.Column(db.TIMESTAMP,
                              default=db.func.utc_timestamp(),
                              onupdate=db.func.utc_timestamp())


class SerializableModelMixin(object):
    def serialize(self,
                  exclude_column_names=None,
                  extra_fields=None):
        if extra_fields is None:
            extra_fields = {}
        if exclude_column_names is None:
            if hasattr(self.__class__, '__exclude_column_names__'):
                exclude_column_names = self.__class__.__exclude_column_names__
            else:
                exclude_column_names = ()

        d = {}
        for column in self.__table__.columns:
            if column.name in exclude_column_names:
                continue

            value = getattr(self, column.name)

            # dateteime -> timestamp
            # date -> yyyy-mm-dd
            if isinstance(value, datetime.datetime):
                value = timegm(value.utctimetuple())
            elif isinstance(value, datetime.date):
                value = value.isoformat()

            if isinstance(column.type, db.Boolean) and value is None:
                value = False

            d[SerializableModelMixin.to_camelcase(column.name)] = value

        d.update(extra_fields)

        return d

    @staticmethod
    def serialize_row(joined_resource_tuple, main_resource_index=0):
        resource_tuple = joined_resource_tuple
        l = list(resource_tuple)  # immutable to mutable l = [user, sem, team]
        main_resource = l.pop(main_resource_index)  # l = [ sem, team]
        d = main_resource.serialize()  # d = {user ..}
        for row in l:
            if row is None:
                continue

            if not hasattr(row, '__table__'): #테이블이 아니라 컬럼일 떄
                continue

            key = SerializableModelMixin.to_camelcase(row.__table__.name)
            d[key] = row.serialize() if row is not None else None

        return d

    @staticmethod
    def to_camelcase(s):
        return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)

    @staticmethod
    def to_snakecase(s):
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()
