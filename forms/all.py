from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class BuyForm(FlaskForm):
    race = SelectField('Раса', choices=[
        (1, 'Бомжи'), (2, 'Интеллигенты'), (3, 'Гопники'), (4, 'Кавказцы')
    ], validators=[DataRequired()])
    number = IntegerField('Кол-во юнитов', validators=[DataRequired()])
    submit = SubmitField('Нанять')

from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')
    
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class RaidForm(FlaskForm):
    users = RadioField('На кого можно напасть:', choices=[], validators=[DataRequired()])
    submit = SubmitField('Напасть!')

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpgradeForm(FlaskForm):
    race_upg = SelectField('Раса', choices=[
        (1, 'Бомжи'), (2, 'Интеллигенты'), (3, 'Гопники'), (4, 'Кавказцы')
    ], validators=[DataRequired()])
    submit_upg = SubmitField('Увеличить мощь!')
