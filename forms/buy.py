from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class BuyForm(FlaskForm):
    race = SelectField('Раса', choices=[
        (1, 'Бомжи'), (2, 'Интеллигенты'), (3, 'Гопники'), (4, 'Кавказцы')
    ], validators=[DataRequired()])
    number = IntegerField('Кол-во юнитов', validators=[DataRequired()])
    submit = SubmitField('Нанять')
