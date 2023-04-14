from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField("Имя пользователя", validators=[DataRequired()])
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_repeat = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class LoginForm(FlaskForm):
    email = StringField("Почта пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField("Войти")
