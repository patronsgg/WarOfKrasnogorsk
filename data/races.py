import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class Race(SqlAlchemyBase):
    __tablename__ = 'races'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    cost = sa.Column(sa.Integer, nullable=True)
    attack = sa.Column(sa.Integer, nullable=True)
    defense = sa.Column(sa.Integer, nullable=True)
    income = sa.Column(sa.Integer, nullable=True)
