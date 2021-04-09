import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Player(SqlAlchemyBase):
    __tablename__ = 'players'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    start_area = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
#   count_army = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user = orm.relation('User')
