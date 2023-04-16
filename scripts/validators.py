from wtforms.validators import StopValidation
from string import punctuation, digits
from models import db_session
from models.users import User

DISALLOWED_PUNCTUATION = punctuation.replace("-", "", 1) \
                                    .replace("_", "", 1) \
                                    .replace(".", "", 1)


def PasswordTemplateValidator():
    NEED_DIGIT = "В пароле должна быть хоть одна цифра"
    NEED_LOWER = "В пароле должна быть хоть одна прописная"
    NEED_UPPER = "В пароле должна быть хоть одна заглавная"

    def validator(_, field):
        hasLower = hasUpper = hasDigit = False
        for symbol in field.data:
            if symbol.islower():
                hasLower = True
            elif symbol.isupper():
                hasUpper = True
            elif symbol.isdigit():
                hasDigit = True

            if hasLower and hasUpper and hasDigit:
                return True

        if not hasDigit:
            raise StopValidation(NEED_DIGIT)
        if not hasUpper:
            raise StopValidation(NEED_UPPER)
        if not hasLower:
            raise StopValidation(NEED_LOWER)
        return True

    return validator


def LoginTemplateValidator():
    STARTS_WITH_DIGIT = "Логин не может начинатся с цифры"
    ENDS_WITH_DOT = "Логин не может заканчиваться точкой"
    HAS_PUNCTUATION = "Нельзя использовать '{}' в логине"
    HAS_ASTERISK = "В логине недопустим символ @"
    HAS_SPACE = "Пробел в логине недопустим"

    def validator(_, field):
        login = field.data

        if login[0] in digits:
            raise StopValidation(STARTS_WITH_DIGIT)

        if login.find("@") != -1:
            raise StopValidation(HAS_ASTERISK)

        if login.find(" ") != -1 or login.find("\n") != -1:
            raise StopValidation(HAS_SPACE)

        if login.endswith("."):
            raise StopValidation(ENDS_WITH_DOT)

        for symbol in login:
            if symbol in DISALLOWED_PUNCTUATION:
                raise StopValidation(HAS_PUNCTUATION.format(symbol))

        return True

    return validator


def UnicodeValidator():
    UNICODE_ERROR = "Нельзя использовать юникод символы!"

    def validator(_, field):
        if not field.data.isprintable():
            raise StopValidation(UNICODE_ERROR)
        return True

    return validator


def EmailExistsValidator(shouldExist=False):
    EMAIL_EXISTS = "Эта почта уже зарегистрирована"
    EMAIL_INVALID = "Такой почты не существует. Сначала зарегистрируйте её"

    def validator(_, field):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == field.data).first()

        if shouldExist and not user:
            raise StopValidation(EMAIL_INVALID)
        if not shouldExist and user:
            raise StopValidation(EMAIL_EXISTS)

        return True

    return validator


def LoginExistsValidator(shouldExist=False):
    LOGIN_EXISTS = "Этот логин уже используется"
    LOGIN_INVALID = "Этот логин ещё не занят"

    def validator(_, field):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == field.data).first()

        if not shouldExist and user:
            raise StopValidation(LOGIN_EXISTS)
        if shouldExist and not user:
            raise StopValidation(LOGIN_INVALID)

        return True

    return validator


__all__ = [
    "PasswordTemplateValidator", "LoginTemplateValidator",
    "EmailExistsValidator", "LoginExistsValidator",
    "UnicodeValidator"
]