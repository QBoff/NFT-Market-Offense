from importlib import import_module
from inspect import isclass
from os import walk
from os.path import abspath, basename, dirname, join
from sys import modules

from flask_sqlalchemy.model import Model

__all__ = ('get_models', 'load_models')

# Папка проекта,  приложения
PROJ_DIR = abspath(join(dirname(abspath(__file__)), '../'))
APP_MODULE = basename(PROJ_DIR)


def get_modules(module):
    """Возвращает все .py скрипты, исключая __init__"""
    file_dir = abspath(join(PROJ_DIR, module))
    for root, dirnames, files in walk(file_dir):
        mod_path = '{}{}'.format(APP_MODULE, root.split(PROJ_DIR)[1]).replace('/', '.')
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('__init__'):
                yield '.'.join([mod_path, filename[0:-3]])


def dynamic_loader(module, compare):
    """
        Перебирает все .py файлы в папке `module`, находя все классы == `compare` функции
        Остальные классы/объекты в этой директории будут проигнорированны
        Возвращает уникальные обьекты.
    """

    items = []
    for mod in get_modules(module):
        module = import_module(mod)
        if hasattr(module, '__all__'):
            objs = [getattr(module, obj) for obj in module.__all__]
            items += [o for o in objs if compare(o) and o not in items]
    return items


def get_models():
    """Динамически ищет модели"""
    return dynamic_loader('models', is_model)


def is_model(item):
    """Определяет если `item` is `db.Model`"""
    return isclass(item) and issubclass(item, Model) and not item.__ignore__()


def load_models():
    """
        Загружает все модели проекта в память для дальнейшего управления
        WARNING: Миграции выполнены не будут!
        Для ресета нужно удалить бд или скачать миграционную библиотеку
    """
    for model in get_models():
        setattr(modules[__name__], model.__name__, model)