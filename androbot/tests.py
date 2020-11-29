from unittest import TestCase

from androbot.actions import (
    add_answer,
    add_question,
    add_user,
    get_main_menu,
    get_next_test,
    remove_questions,
    remove_user,
    start_new_test,
)
from androbot.errors import UserExistsException, UserNotExistsException
from androbot.schemas import Answer, Question, TelegramUser
from androbot.specialty import Specialty
from androbot.utils import Utils


class Test(TestCase):
    def test_get_main_menu(self):
        welcome_message = (
            "Привет, я помогу тебе подготовиться к собеседованию\r\nВыбери "
            'специальность:\r\n`Android`\r\n```print("Hello world")``` '
        )

        self.assertEqual(get_main_menu(), [welcome_message.strip(), ["android", "test"]])

    def test_start_new_test(self):
        self.assertEqual(start_new_test(), ["voice", "text", "mental"])

    def test_add_user(self):
        user = TelegramUser(
            tg_user_id=int(Utils.get_random_number(5)),
            name=Utils.get_random_text(10),
            username=Utils.get_random_text(10),
            specialty=Specialty.ANDROID.value,
        )
        db_user = add_user(user)
        self.assertEqual(db_user.tg_user_id, user.tg_user_id)
        remove_user(db_user)

    def test_add_already_exist_user(self):
        user = TelegramUser(
            tg_user_id=int(Utils.get_random_number(5)),
            name=Utils.get_random_text(10),
            username=Utils.get_random_text(10),
            specialty=Specialty.ANDROID.value,
        )
        db_user = add_user(user)
        self.assertEqual(add_user(user), UserExistsException)
        remove_user(db_user)

    def test_remove_not_exist_user(self):
        user = TelegramUser(
            tg_user_id=int(Utils.get_random_number(5)),
            name=Utils.get_random_text(10),
            username=Utils.get_random_text(10),
            specialty=Specialty.ANDROID.value,
        )
        self.assertEqual(remove_user(user), UserNotExistsException)

    def test_get_next_test(self):
        user = TelegramUser(
            tg_user_id=int(Utils.get_random_number(5)),
            name=Utils.get_random_text(10),
            username=Utils.get_random_text(10),
            specialty=Specialty.FOR_TEST.value,
        )
        question1 = Question(
            quest_id=int(Utils.get_random_number(5)),
            question_type=Specialty.FOR_TEST.value,
            text_answer=Utils.get_random_text(10),
        )
        question2 = Question(
            quest_id=int(Utils.get_random_number(5)),
            question_type=Specialty.FOR_TEST.value,
            text_answer=Utils.get_random_text(10),
        )
        question3 = Question(
            quest_id=int(Utils.get_random_number(5)),
            question_type=Specialty.FOR_TEST.value,
            text_answer=Utils.get_random_text(10),
        )
        answer1 = Answer(
            answer_id=int(Utils.get_random_number(5)),
            quest_id=question1.quest_id,
            tg_user_id=user.tg_user_id,
            answer_type=start_new_test()[1],
            text_answer=Utils.get_random_text(50),
            link_to_audio_answer=Utils.get_random_text(50),
        )
        answer2 = Answer(
            answer_id=int(Utils.get_random_number(5)),
            quest_id=question2.quest_id,
            tg_user_id=user.tg_user_id,
            answer_type=start_new_test()[1],
            text_answer=Utils.get_random_text(50),
            link_to_audio_answer=Utils.get_random_text(50),
        )
        answer3 = Answer(
            answer_id=int(Utils.get_random_number(5)),
            quest_id=question1.quest_id,
            tg_user_id=user.tg_user_id,
            answer_type=start_new_test()[1],
            text_answer=Utils.get_random_text(50),
            link_to_audio_answer=Utils.get_random_text(50),
        )
        add_question(question1)
        add_question(question2)
        add_question(question3)
        add_answer(answer1)
        add_answer(answer2)
        add_answer(answer3)
        question = get_next_test(user)
        remove_questions(Specialty.FOR_TEST.value)
        remove_user(user)
        self.assertEqual(question.quest_id, question3.quest_id)
