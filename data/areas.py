import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class Area(SqlAlchemyBase):
    __tablename__ = 'areas'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    race = sa.Column(sa.String, nullable=True)
