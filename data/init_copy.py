from data.users import User
from data.players import Player
from data.races import Race
from data.army import Army
from data import db_session

db_session.global_init('warkrasnogorsk.db')
db_sess = db_session.create_session()

races = [
    Race(title='Бомжи', cost=25, defense=2, attack=4, income=2),
    Race(title='Интеллигенты', cost=15, defense=2, attack=2, income=3),
    Race(title='Гопники', cost=15, defense=1, attack=3, income=3),
    Race(title='Кавказцы', cost=10, defense=2, attack=1, income=4)
]
db_sess.add_all(races)

user = User()
user.username = 'vasya'
user.email = 'abc@abc.org'
user.set_password('123')
db_sess.add(user)

player = Player()
player.user_id = 1
player.money = 100
player.start_race_id = 1
db_sess.add(player)

army = Army()
army.player_id = 1
army.number = 5
army.race_id = 1
army.level = 1
db_sess.add(army)

db_sess.commit()
