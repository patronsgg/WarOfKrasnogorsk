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


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, index=True, unique=True, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    player = orm.relation('Player', uselist=False, back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
