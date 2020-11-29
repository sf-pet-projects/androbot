from unittest import TestCase

from androbot.actions import get_main_menu, start_new_test


class Test(TestCase):
    def test_get_main_menu(self):
        welcome_message = (
            "Привет, я помогу тебе подготовиться к собеседованию\r\nВыбери "
            'специальность:\r\n`Android`\r\n```print("Hello world")``` '
        )

        self.assertEqual(get_main_menu(), [welcome_message.strip(), ["android"]])

    def test_start_new_test(self):
        self.assertEqual(start_new_test(), ["voice", "text", "mental"])
