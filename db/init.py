from data.users import User
from data.players import Player
from data.races import Race
from data import db_session

db_session.global_init('warkrasnogorsk.db')
db_sess = db_session.create_session()

areas = [
    Race(title='Бомжи'),
    Race(title='Интеллигенты'),
    Race(title='Гопники'),
    Race(title='Кавказцы')
]
db_sess.add_all(areas)

user = User()
user.username = 'vasya'
user.email = 'abc@abc.org'
user.set_password('123')
db_sess.add(user)

player = Player()
player.user_id = 1
player.money = 1000
player.start_race_id = 1
db_sess.add(player)

db_sess.commit()
