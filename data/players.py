import sqlalchemy as sa
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Player(SqlAlchemyBase):
    __tablename__ = 'players'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    start_race_id = sa.Column(sa.Integer, sa.ForeignKey('races.id'))
    money = sa.Column(sa.Integer, nullable=True)
    user = orm.relation('User', back_populates='player')
    start_race = orm.relation('Race')