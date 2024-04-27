from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired, Length, Regexp, InputRequired, ValidationError


def double(x):
    res = x * 2
    if res > 9:
        res = res - 9
    return res


def luhn_algorithm(card):
    card = [i for i in card.split()]
    odd = map(lambda x: double(int(x)), card[::2])
    even = map(int, card[1::2])
    return (sum(odd) + sum(even)) % 10 == 0


def luhn_algorithm_check():
    message = 'Неправельный номер карты.'

    def _luhn_algorithm_check(form, field):
        if luhn_algorithm(field.data):
            raise ValidationError(message)

    return _luhn_algorithm_check


class PayCard(FlaskForm):
    money = IntegerField('Сумма в ₽', validators=[DataRequired(), InputRequired()])
    bankcard_number = StringField('Номер банковской карты',
                                  validators=[DataRequired(), InputRequired(), Length(min=16, max=19),
                                              Regexp(
                                                  regex=r"^\d{4}[ ]{1}\d{4}[ ]{1}\d{4}[ ]{1}\d{4}$",
                                                  message="Valid bankcard number format is xxxx xxxx xxxx xxxx"
                                              ), luhn_algorithm_check()])
    yy_mm = StringField('YY_MM', validators=[DataRequired(), InputRequired(), Length(min=4, max=5),
                                             Regexp(regex=r"^\d{2}[ ]{1}\d{2}$", message="Valid yy_mm format is xx xx"
                                                    )])
    cvc = StringField('CVC', validators=[DataRequired(), Length(min=3, max=3), InputRequired()])
    submit = SubmitField('Оплатить картой')
