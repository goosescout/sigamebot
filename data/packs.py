import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Pack(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'packs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    game = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    user = orm.relation('User')

    def __repr__(self):
        return f'{self.surname} {self.name}'
