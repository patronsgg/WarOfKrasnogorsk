import threading
from data import db_session
from data.players import Player


def get_money():
    db_sess = db_session.create_session()
    players = db_sess.query(Player).all()
    for x in players:
        count = 0
        for item in x.army:
            count += (item.number * item.race.income)
        x.money += count
    db_sess.commit()
    threading.Timer(60, get_money).start()


def main():
    db_session.global_init('db/warkrasnogorsk.db')
    get_money()
