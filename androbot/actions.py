import codecs
from .specialty import Specialty


def get_main_menu():
    with codecs.open("welcome.message", "r", encoding='utf-8') as file:
        welcome_message = file.read()
        return [welcome_message, [e.value for e in Specialty]]
