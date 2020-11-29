from unittest import TestCase

from androbot.actions import add_user, get_main_menu, remove_user, start_new_test
from androbot.errors import UserExistsException, UserNotExistsException
from androbot.schemas import TelegramUser
from androbot.utils import Utils


class Test(TestCase):
    def test_get_main_menu(self):
        welcome_message = (
            "Привет, я помогу тебе подготовиться к собеседованию\r\nВыбери "
            'специальность:\r\n`Android`\r\n```print("Hello world")``` '
        )

        self.assertEqual(get_main_menu(), [welcome_message.strip(), ["android"]])

    def test_start_new_test(self):
        self.assertEqual(start_new_test(), ["voice", "text", "mental"])

    def test_add_user(self):
        user = TelegramUser(
            tg_user_id=int(Utils.get_random_number()),
            name=Utils.get_random_text(),
            username=Utils.get_random_text(),
        )
        db_user = add_user(user)
        self.assertEqual(db_user.tg_user_id, user.tg_user_id)
        remove_user(db_user)

    def test_add_already_exist_user(self):
        user = TelegramUser(
            tg_user_id=int(Utils.get_random_number()),
            name=Utils.get_random_text(),
            username=Utils.get_random_text(),
        )
        db_user = add_user(user)
        self.assertEqual(add_user(user), UserExistsException)
        remove_user(db_user)

    def test_remove_not_exist_user(self):
        user = TelegramUser(
            tg_user_id=int(Utils.get_random_number()),
            name=Utils.get_random_text(),
            username=Utils.get_random_text(),
        )
        self.assertEqual(remove_user(user), UserNotExistsException)
