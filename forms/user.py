from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Regexp, InputRequired, EqualTo


class RegisterForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired(), InputRequired(),
                                                   EqualTo('password_again', message='Пароли должны совпадать')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    phone_number = StringField('Номер телефона',
                               validators=[DataRequired(), Length(min=10, max=14), Regexp(regex='^[+-]?[0-9]+$')])
    submit = SubmitField('Войти')
