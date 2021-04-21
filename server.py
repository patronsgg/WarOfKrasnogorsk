from flask import Flask, render_template, abort
from werkzeug.utils import redirect
from data.users import User
from data.players import Player
from data.races import Race
from data.army import Army
from data import db_session
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.buy import BuyForm
from forms.upgrade import UpgradeForm
from forms.raid import RaidForm
from flask_login import login_user, LoginManager, logout_user, \
    login_required, current_user
from get_money import main
from random import choice, random
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abobaABOBAaboba'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def root():
    if current_user.is_authenticated:
        if not current_user.player:
            return render_template('main.html')
        db_sess = db_session.create_session()
        message_buy, message_upg = '', ''
        other = ([(x.race.title, x.number) for x in current_user.player.army], current_user.player.money,
                 sum([(x.number * x.race.bring_money) for x in current_user.player.army]),
                 sum([x.number * x.race.power * (x.upgrade_lvl if x.upgrade_lvl == 1 else x.upgrade_lvl * 2)
                      for x in current_user.player.army]))

        player = db_sess.query(Player).get(current_user.id)
        available_races = [army.race_id for army in player.army]
        buy_form = BuyForm()
        buy_form.race.choices = list(filter(lambda x: x[0] in available_races, buy_form.race.choices))
        if buy_form.validate_on_submit() and buy_form.submit.data:
            race_id, number = int(buy_form.race.data), buy_form.number.data
            race = db_sess.query(Race).get(race_id)
            if race.cost * number > player.money:
                message_buy = 'Недостаточно денег!'
            else:
                player.money -= race.cost * number
                army = list(filter(lambda x: x.race_id == race_id, player.army))[0]
                army.number += number
                db_sess.commit()

        available_races = [army.race_id for army in player.army]
        upgrade_form = UpgradeForm()
        upgrade_form.race_upg.choices = list(filter(lambda x: x[0] in available_races, upgrade_form.race_upg.choices))
        if upgrade_form.validate_on_submit() and upgrade_form.submit_upg.data:
            race_id = int(upgrade_form.race_upg.data)
            army_list = list(filter(lambda x: x.race_id == race_id, player.army))[0]
            if army_list.upgrade_lvl >= 3:
                message_upg = 'Достигнут максимальный уровень!'
            elif (1.4 if army_list.upgrade_lvl == 1 else 1.8) * army_list.number > player.money:
                message_upg = 'Недостаточно денег!'
            else:
                player.money -= (1.25 if army_list.upgrade_lvl == 1 else 1.6) * army_list.number
                army_list.upgrade_lvl += 1
                db_sess.commit()
        return render_template('main.html', buy_form=buy_form, upgrade_form=upgrade_form, other=other,
                               message_buy=message_buy, message_upg=message_upg)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if (db_sess.query(User).filter(User.email == form.email.data).first()) or \
                (db_sess.query(User).filter(User.username == form.username.data).first()):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Такой пользователь уже есть')
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/choose_area/<int:id>')
@login_required
def choose_area(id):
    if current_user.player:
        return abort(404)
    db_sess = db_session.create_session()
    if not db_sess.query(Race).get(id):
        return abort(404)
    player = Player(
        user_id=current_user.id,
        money=100,
        start_race_id=id
    )
    db_sess.add(player)
    db_sess.commit()
    army = Army(
        player_id=player.id,
        race_id=id,
        number=5,
        upgrade_lvl=1
    )
    db_sess.add(army)
    db_sess.commit()
    return redirect('/')


@app.route('/leadersboard')
@login_required
def leaders_board():
    db_sess = db_session.create_session()
    users = [x for x in db_sess.query(User).all() if x.player]
    leaders = []
    for x in users:
        leaders.append((x.username, sum([item.number for item in x.player.army]), x.player.money))
    leaders.sort(key=lambda x: (-x[1], -x[2], x[0]))
    return render_template('leadersboard.html', leaders=leaders)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/raid', methods=['GET', 'POST'])
@login_required
def raid():
    db_sess = db_session.create_session()

    available_users = [user.username for user in db_sess.query(User).all() if user.id != current_user.id
                       and user.player and check_time(user.player.last_defend)]
    raidform = RaidForm()
    raidform.users.choices = available_users
    if raidform.validate_on_submit():
        message = ''
        username = raidform.users.data
        user_attack = db_sess.query(User).filter(User.username == current_user.username).first()
        user_defend = db_sess.query(User).filter(User.username == username).first()
        army_attack = user_attack.player.army
        army_defend = user_defend.player.army
        power_attack = sum([(item.number * item.race.power * (item.upgrade_lvl
                                                              if item.upgrade_lvl == 1 else item.upgrade_lvl * 2)) for
                            item in army_attack])
        defence_defend = sum([(x.number * x.race.defence * (x.upgrade_lvl
                                                            if x.upgrade_lvl == 1 else x.upgrade_lvl * 2)) for x in
                              army_defend])
        chance = random()
        if power_attack > defence_defend and (power_attack == defence_defend and chance >= 0.5):
            new_race = choice(army_defend)
            ratio = random()
            if new_race.race_id not in [x.race_id for x in army_attack]:
                prize = Army(
                    player_id=user_attack.player.id,
                    race_id=new_race.race_id,
                    number=round(new_race.number * ratio),
                    upgrade_lvl=1
                )
                db_sess.add(prize)
            else:
                army_to_edit = choice(army_attack)
                army_to_edit.number += round(new_race.number * ratio)
            user_defend.player.last_defend = datetime.now()
            new_race.number -= round((ratio * new_race.number))
            money = user_defend.player.money // 2
            user_defend.player.money -= money
            user_attack.player.money += money
            message = 'Рейд прошел успешно. Вы получили деньги и юнитов'
        else:
            ratio = random()
            army = choice(army_attack)
            army.number -= round(army.number * ratio)
            user_attack.player.money -= round(user_attack.player.money * ratio)
            message = 'Вы проиграли рейд. У вас забрали часть юнитов и денег'
        db_sess.commit()
        return render_template('raid.html', raidform=raidform, message=message)
    return render_template('raid.html', raidform=raidform)


def check_time(last_defend):
    if last_defend is None:
        return True
    if datetime.now() - last_defend > timedelta(hours=0, minutes=10):
        return True
    return False


if __name__ == '__main__':
    main()
    db_session.global_init('db/warkrasnogorsk.db')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
