from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired, Length, Regexp


class LoginForm(FlaskForm):
    phone_number = StringField('Номер телефона',
                               validators=[DataRequired(), Length(min=10, max=14), Regexp(regex='^[+-]?[0-9]+$')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
