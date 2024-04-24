from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class AddLotsForm(FlaskForm):
    quantity = IntegerField('Количество ГБ', validators=[DataRequired()])
    price = IntegerField('Cтоимость за один гб', validators=[DataRequired()])
    submit = SubmitField('Создать')
