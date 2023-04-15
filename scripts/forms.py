from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField("Имя пользователя", validators=[DataRequired()])
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    wallet = StringField("Крипто-кошелёк", validators=[DataRequired()])
    submit = SubmitField("Войти")


class LoginForm(FlaskForm):
    email = StringField("Почта пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")
