from flask import Flask, render_template, abort
from werkzeug.utils import redirect
from data.users import User
from data.players import Player
from data.races import Race
from data.army import Army
from data.raids import Raid
from data import db_session
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.buy import BuyForm
from forms.upgrade import UpgradeForm
from forms.raid import RaidForm
from flask_login import login_user, LoginManager, logout_user, \
    login_required, current_user
from get_money import main
from random import choice, uniform
from math import ceil, floor
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
        player = db_sess.query(Player).get(current_user.id)
        total_attack = sum([get_stats_with_upgrades(x)[0] for x in player.army])
        total_defense = sum([get_stats_with_upgrades(x)[1] for x in player.army])
        army_power = (total_attack + total_defense) // 2
        other = (
            [(x.race.title, x.number) for x in player.army], player.money,
            sum([(x.number * x.race.income) for x in player.army]), army_power
        )
        available_races = [army.race_id for army in player.army]
        buy_form = BuyForm()
        buy_form.race.choices = list(filter(lambda x: x[0] in available_races, buy_form.race.choices))

        available_races = [army.race_id for army in player.army if army.level != 3]
        upgrade_form = UpgradeForm()
        upgrade_form.race_upg.choices = list(filter(lambda x: x[0] in available_races, upgrade_form.race_upg.choices))

        if buy_form.validate_on_submit() and buy_form.submit.data:
            race_id, number = int(buy_form.race.data), buy_form.number.data
            race = db_sess.query(Race).get(race_id)
            if race.cost * number > player.money:
                return render_template('main.html', buy_form=buy_form, upgrade_form=upgrade_form, other=other,
                                       message_buy='???????????????????????? ??????????!')
            else:
                player.money -= race.cost * number
                army = list(filter(lambda x: x.race_id == race_id, player.army))[0]
                army.number += number
                db_sess.commit()
                return redirect('/')

        if upgrade_form.validate_on_submit() and upgrade_form.submit_upg.data:
            race_id = int(upgrade_form.race_upg.data)
            army = list(filter(lambda x: x.race_id == race_id, player.army))[0]
            if army.level == 3:
                return render_template('main.html', buy_form=buy_form, upgrade_form=upgrade_form, other=other,
                                       message_upg='?????????????????? ???????????????????????? ??????????????!')
            else:
                total = 0
                if army.level == 2:
                    total = army.number * army.race.cost * 2 + 2500
                elif army.level == 1:
                    total = army.number * army.race.cost + 1000
                if total > player.money:
                    return render_template('main.html', buy_form=buy_form, upgrade_form=upgrade_form, other=other,
                                           message_upg='???????????????????????? ??????????!')
                else:
                    player.money -= total
                    army.level += 1
                    db_sess.commit()
                    return redirect('/')
        return render_template('main.html', buy_form=buy_form, upgrade_form=upgrade_form, other=other)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return abort(404)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message='???????????? ???? ??????????????????')
        db_sess = db_session.create_session()
        if (db_sess.query(User).filter(User.email == form.email.data).first()) or \
                (db_sess.query(User).filter(User.username == form.username.data).first()):
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message='?????????? ???????????????????????? ?????? ????????')
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='??????????????????????', form=form)


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
                               message='???????????????????????? ?????????? ?????? ????????????',
                               form=form)
    return render_template('login.html', title='??????????????????????', form=form)


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
        level=1
    )
    db_sess.add(army)
    db_sess.commit()
    return redirect('/')


@app.route('/leadersboard')
@login_required
def leaders_board():
    db_sess = db_session.create_session()
    players = db_sess.query(Player).all()
    leaders = []
    for player in players:
        leaders.append((
            player.user.username, sum([item.number for item in player.army]),
            get_full_army_power(player.army), player.money
        ))
    leaders.sort(key=lambda x: (-x[2], -x[1], -x[3], x[0]))
    return render_template('leadersboard.html', leaders=leaders)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/raid', methods=['GET', 'POST'])
@login_required
def raid():
    db_sess = db_session.create_session()
    available_users = []
    for user in db_sess.query(User).all():
        if user.id == current_user.id or not user.player:
            continue
        if not check_time(user.player.last_defend):
            continue
        available_users.append(
            (user.username, f'{user.username} (???????? ??????????: {get_full_army_power(user.player.army)})')
        )
    raidform = RaidForm()
    raidform.users.choices = available_users
    player = db_sess.query(Player).get(current_user.id)
    attack_raids = db_sess.query(Raid).filter(Raid.attacker_id == player.id)
    defense_raids = db_sess.query(Raid).filter(Raid.defender_id == player.id)
    if raidform.validate_on_submit():
        raid_ = Raid()
        message = ''
        username = raidform.users.data
        attacker = player
        defender = db_sess.query(User).filter(User.username == username).first().player
        raid_.attacker_id, raid_.defender_id = attacker.id, defender.id
        army_attacker = attacker.army
        army_defender = defender.army
        total_attack = sum([get_stats_with_upgrades(x)[0] for x in army_attacker])
        total_defense = sum([get_stats_with_upgrades(x)[1] for x in army_defender])
        chance_attacker, chance_defender = uniform(0.75, 1.0), uniform(0.75, 1.0)
        diff = round(total_attack * chance_attacker - total_defense * chance_defender)
        if diff > 0:
            message += '???????? ???????????? ??????????????! ???? ???????????????? ?????????? ?????????? ?? ?????????? ??????????????????.'
            raid_.is_success = True
            withdraw_money = round(defender.money * uniform(0.25, 0.45))
            raid_.withdraw_money = withdraw_money
            prize_army = choice([x for x in army_defender])
            prize_army_number = ceil(uniform(0.1, 0.2) * prize_army.number)
            losses = raid_losses(attacker, defender)
            raid_.losses_att, raid_.losses_def = sum(losses[0]), sum(losses[1])
            attacker.money += withdraw_money
            defender.money -= withdraw_money
            if prize_army.race_id not in [x.race_id for x in army_attacker]:
                prize = Army(
                    player_id=attacker.id,
                    race_id=prize_army.race_id,
                    number=prize_army_number,
                    level=1
                )
                db_sess.add(prize)
                message += f' ???? ?????????????? ?????????? ???????? - {prize_army.race.title}!'
            else:
                army_to_add = list(filter(lambda x: x.race_id == prize_army.race_id, army_attacker))[0]
                army_to_add.number += prize_army_number
            raid_.prize_race_title = prize_army.race.title
            raid_.prize_race_number = prize_army_number
            defender.last_defend = datetime.now()
        else:
            raid_.is_success = False
            losses = raid_losses(defender, attacker)
            raid_.losses_att, raid_.losses_def = sum(losses[1]), sum(losses[0])
            message += '???????? ???????????????????? ????????????????. ???? ???????????????? ?????????? ?????????? ??????????.'
        db_sess.add(raid_)
        db_sess.commit()
        return render_template(
            'raid.html', raidform=raidform, message=message, raids=(attack_raids, defense_raids))
    return render_template('raid.html', raidform=raidform, raids=(attack_raids, defense_raids))


def check_time(last_defend):
    if last_defend is None:
        return True
    if datetime.now() - last_defend > timedelta(hours=0, minutes=10):
        return True
    return False


def raid_losses(winner, loser):
    losses_loser = [round(x.number * uniform(0.4, 0.5)) for x in loser.army]
    total_losses_loser, winner_army_num = sum(losses_loser), len(winner.army)
    max_army_losses_winner = total_losses_loser // winner_army_num
    losses_winner = [floor(uniform(0.75, 0.85) * max_army_losses_winner) for _ in winner.army]
    for i, army in enumerate(winner.army):
        army.number -= losses_winner[i]
    for i, army in enumerate(loser.army):
        army.number -= losses_loser[i]
    return losses_winner, losses_loser


def get_stats_with_upgrades(army):
    total_attack = army.number * army.race.attack * (army.level if army.level == 1 else army.level * 2)
    total_defense = army.number * army.race.defense * (army.level if army.level == 1 else army.level * 2)
    return total_attack, total_defense


def get_full_army_power(army_list):
    total_attack = sum([get_stats_with_upgrades(x)[0] for x in army_list])
    total_defense = sum([get_stats_with_upgrades(x)[1] for x in army_list])
    return (total_attack + total_defense) // 2


if __name__ == '__main__':
    main()
    db_session.global_init('db/warkrasnogorsk.db')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
