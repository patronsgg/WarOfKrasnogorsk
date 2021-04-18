import threading
from data import db_session
from data.users import User


def get_money():
    db_sess = db_session.create_session()
    army = [(x, sum((item.number for item in x.player.army))) for x in db_sess.query(User).all()]
    for x in army:
        x[0].player.money += x[1]
    db_sess.commit()
    threading.Timer(60, get_money).start()


def main():
    db_session.global_init('db/warkrasnogorsk.db')
    get_money()