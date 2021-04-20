import sqlalchemy as sa
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Army(SqlAlchemyBase):
    __tablename__ = 'army'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey('players.id'))
    race_id = sa.Column(sa.Integer, sa.ForeignKey('races.id'))
    number = sa.Column(sa.Integer, nullable=True)
    upgrade_lvl = sa.Column(sa.Integer, nullable=True)

    race = orm.relation('Race')
    player = orm.relation('Player', back_populates='army')
