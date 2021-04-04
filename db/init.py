from data.users import User
from data import db_session

user = User()
user.name = "Pushkin"
user.email = "email@email.ru"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()