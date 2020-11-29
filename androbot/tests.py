from unittest import TestCase

from androbot.actions import get_main_menu


class Test(TestCase):
    def test_get_main_menu(self):
        welcome_message = (
            "Привет, я помогу тебе подготовиться к собеседованию\r\nВыбери "
            'специальность:\r\n`Android`\r\n```print("Hello world")``` '
        )

        self.assertEqual(get_main_menu(), [welcome_message.strip(), ["android"]])
