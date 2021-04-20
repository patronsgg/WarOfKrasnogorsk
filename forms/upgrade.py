from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class UpgradeForm(FlaskForm):
    race_upg = SelectField('Раса', choices=[
        (1, 'Бомжи'), (2, 'Интеллигенты'), (3, 'Гопники'), (4, 'Кавказцы')
    ], validators=[DataRequired()])
    submit_upg = SubmitField('Увеличить мощь!')
