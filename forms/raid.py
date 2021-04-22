from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class RaidForm(FlaskForm):
    users = RadioField('На кого можно напасть:', choices=[], validators=[DataRequired()])
    submit = SubmitField('Напасть!')
