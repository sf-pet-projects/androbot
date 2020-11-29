from unittest import TestCase

from androbot.actions import get_main_menu


class Test(TestCase):
    def test_get_main_menu(self):
        self.assertEqual(get_main_menu(), ["Привет, я помогу тебе подготовиться к собеседованию\r\nВыбери "
                                           "специальность:\r\n`Android`\r\n```print(\"Hello world\")```", ['android']])
