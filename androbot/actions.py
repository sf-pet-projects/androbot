import codecs

from .config import settings
from .specialty import Specialty


def get_main_menu():
    with codecs.open("welcome.message", "r", encoding="utf-8") as file:
        welcome_message = file.read()
        return [welcome_message, [e.value for e in Specialty]]


def start_new_test():
    return list(map(lambda x: x.strip(), settings.answers_types.split(",")))
