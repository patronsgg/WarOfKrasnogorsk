import sqlalchemy as sa
from sqlalchemy import orm
import datetime
from .db_session import SqlAlchemyBase


class Army(SqlAlchemyBase):
    __tablename__ = 'army'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey('players.id'))
    race_id = sa.Column(sa.Integer, sa.ForeignKey('races.id'))
    number = sa.Column(sa.Integer, nullable=True)
    level = sa.Column(sa.Integer, nullable=True)

    race = orm.relation('Race')
    player = orm.relation('Player', back_populates='army')


class Raid(SqlAlchemyBase):
    __tablename__ = 'raids'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    attacker_id = sa.Column(sa.Integer, sa.ForeignKey('players.id'))
    defender_id = sa.Column(sa.Integer, sa.ForeignKey('players.id'))
    is_success = sa.Column(sa.Boolean, nullable=True)
    losses_att = sa.Column(sa.Integer, nullable=True)
    losses_def = sa.Column(sa.Integer, nullable=True)
    withdraw_money = sa.Column(sa.Integer, nullable=True)
    prize_race_title = sa.Column(sa.String, nullable=True)
    prize_race_number = sa.Column(sa.Integer, nullable=True)
    occurrence_date = sa.Column(sa.DateTime, default=datetime.datetime.now)

    attacker = orm.relation('Player', foreign_keys=[attacker_id])
    defender = orm.relation('Player', foreign_keys=[defender_id])