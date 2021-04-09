import sqlalchemy as sa
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Player(SqlAlchemyBase):
    __tablename__ = 'players'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    start_area_id = sa.Column(sa.Integer, sa.ForeignKey('areas.id'))
    money = sa.Column(sa.Integer, nullable=True)
#   count_army = sa.Column(sa.Integer, nullable=True)
    user = orm.relation('User', back_populates='player')
    start_area = orm.relation('Area')
