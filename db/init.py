from data.users import User
from data.players import Player
from data.races import Race
from data.army import Army
from data import db_session

db_session.global_init('warkrasnogorsk.db')
db_sess = db_session.create_session()

areas = [
    Race(title='Бомжи', cost=5, defence=2, power=4, bring_money=2),
    Race(title='Интеллигенты', cost=3, defence=2, power=2, bring_money=3),
    Race(title='Гопники', cost=3, defence=1, power=3, bring_money=3),
    Race(title='Кавказцы', cost=2, defence=2, power=1, bring_money=4)
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

army = Army()
army.player_id = 1
army.number = 5
army.race_id = 1
army.upgrade_lvl = 1
db_sess.add(army)

db_sess.commit()
