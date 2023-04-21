from flask_wtf import FlaskForm
from validators import (EmailExistsValidator, LoginExistsValidator,
                        LoginTemplateValidator, PasswordTemplateValidator,
                        UnicodeValidator)
from wtforms import (EmailField, FileField, FloatField, PasswordField,
                     StringField, SubmitField, BooleanField, TextAreaField)
from wtforms.validators import Email, InputRequired, Length, NumberRange, DataRequired

from models.nfts import NFT
from models.users import User

MAX_EMAIL_LENGTH = User.email.type.length
MAX_LOGIN_LENGTH = User.login.type.length
MAX_NFT_NAME_LENGTH = NFT.name.type.length
MIN_LOGIN_LENGTH = 5
MIN_PASSWORD_LENGTH = 8

NEGATIVE_NUM_ERROR = "Цена не может быть отрицательной или состоять из букв"
NFT_NAME_MISSING = "Необходимо указать название NFT"
NFT_COST_MISSING = "Не указана цена NFT"
NFT_FILE_MISSING = "Файл NFT не опубликован"
NFT_LEN_ERROR = "Длина названия превышена"
EMAIL_MISSING = "Почта не заполнена"
EMAIL_INVALID = "Неверный формат почты"
LOGIN_MISSING = "Логин не заполнен"
LOGIN_LEN_ERROR = "Логин должен быть от {} до {} символов".format(
                  MIN_LOGIN_LENGTH, MAX_LOGIN_LENGTH)
PASS_MISSING = "Поле с паролем пустое"
PASS_LEN_ERROR = "Длина пароля должна составлять минимум {} символов!".format(
                 MIN_PASSWORD_LENGTH)
del NFT


class RegisterForm(FlaskForm):
    login = StringField("Имя пользователя", validators=[
        InputRequired(LOGIN_MISSING),
        Length(
            min=MIN_LOGIN_LENGTH,
            max=MAX_LOGIN_LENGTH,
            message=LOGIN_LEN_ERROR
        ),
        UnicodeValidator(),
        LoginTemplateValidator(),
        LoginExistsValidator(shouldExist=False)
    ])

    email = EmailField("Почта", validators=[
        InputRequired(EMAIL_MISSING),
        Length(
            max=MAX_EMAIL_LENGTH,
            message=EMAIL_INVALID
        ),
        Email(EMAIL_INVALID),
        EmailExistsValidator(shouldExist=False)
    ])

    password = PasswordField("Пароль", validators=[
        InputRequired(PASS_MISSING),
        Length(
            min=MIN_PASSWORD_LENGTH,
            message=PASS_LEN_ERROR
        ),
        UnicodeValidator(),
        PasswordTemplateValidator()]
    )

    wallet = StringField("Крипто-кошелёк", validators=[InputRequired()])
    submit = SubmitField("Войти")


class LoginForm(FlaskForm):
    email = StringField("Почта пользователя", validators=[
        InputRequired(EMAIL_MISSING),
        EmailExistsValidator(shouldExist=True)
    ])
    password = PasswordField("Пароль", validators=[
        InputRequired(PASS_MISSING)]
    )

    submit = SubmitField("Войти")


class NFTCreationForm(FlaskForm):
    name = StringField("Имя", validators=[
        InputRequired(NFT_NAME_MISSING),
        Length(
            max=MAX_NFT_NAME_LENGTH,
            message=NFT_LEN_ERROR)
    ])

    cost = FloatField("Цена", validators=[
        InputRequired(NFT_COST_MISSING),
        NumberRange(
            min=0,
            message=NEGATIVE_NUM_ERROR
        )
    ])

    description = TextAreaField("Описание", validators=[
        InputRequired("Вы забыли описание"),
        Length(max=300)
    ])

    is_selling = BooleanField("Выставить на продажу")
    image = FileField("Изображение NFT", validators=[DataRequired(NFT_FILE_MISSING)])
    submit = SubmitField("Выставить на продажу")


__all__ = ["LoginForm", "NFTCreationForm", "RegisterForm"]