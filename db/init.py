from data.users import User
from data.players import Player
from data.areas import Area
from data import db_session

db_session.global_init('warkrasnogorsk.db')
db_sess = db_session.create_session()

areas = [
    Area(title='Чернево-1', race='Бомжи'),
    Area(title='Чернево-2', race='Интеллигенты'),
    Area(title='Бруски', race='Гопники'),
    Area(title='Изумрудки', race='Кавказцы')
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
player.start_area_id = 1
db_sess.add(player)

db_sess.commit()
