import sqlalchemy as sa
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Army(SqlAlchemyBase):
    __tablename__ = 'armies'

    player_id = sa.Column(sa.Integer, sa.ForeignKey('players.id'))
    race_id = sa.Column(sa.Integer, sa.ForeignKey('races.id'))
    number = sa.Column(sa.Integer, nullable=True)

    race = orm.relation('Race')
    player = orm.relation('Player', back_populates='army')