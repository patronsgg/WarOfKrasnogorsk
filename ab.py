
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
                message += f' Вы открыли новую расу - {prize_army.race.title}!'
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
            message += 'Рейд завершился неудачей. Вы потеряли часть своей армии.'
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
