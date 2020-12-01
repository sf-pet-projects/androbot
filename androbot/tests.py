from androbot.actions import (
    add_answer,
    add_question,
    add_user,
    get_main_menu,
    get_next_test,
    get_test_result,
    remove_questions,
    remove_user,
    start_new_test,
)
from androbot.errors import UserExistsException, UserNotExistsException
from androbot.schemas import Answer, Question, TelegramUser
from androbot.specialty import Specialty
from androbot.utils import Utils


def test_get_main_menu():
    assert get_main_menu() == ["Android Developer", "test"]


def test_start_new_test():
    assert start_new_test() == ["voice", "text", "mental"]


def test_add_user():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    db_user = add_user(user)
    assert db_user.tg_user_id == user.tg_user_id
    remove_user(db_user)


def test_add_already_exist_user():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    add_user(user)
    try:
        add_user(user)
        assert False
    except UserExistsException:
        assert True


def test_remove_not_exist_user():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    try:
        remove_user(user)
        assert False
    except UserNotExistsException:
        assert True


def test_get_next_test():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.FOR_TEST.value,
    )
    question1 = Question(
        quest_id=Utils.get_random_number(5),
        question_type=Specialty.FOR_TEST.value,
        text_answer=Utils.get_random_text(10),
    )
    question2 = Question(
        quest_id=Utils.get_random_number(5),
        question_type=Specialty.FOR_TEST.value,
        text_answer=Utils.get_random_text(10),
    )
    question3 = Question(
        quest_id=Utils.get_random_number(5),
        question_type=Specialty.FOR_TEST.value,
        text_answer=Utils.get_random_text(10),
    )
    answer1 = Answer(
        answer_id=Utils.get_random_number(5),
        quest_id=question1.quest_id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
    )
    answer2 = Answer(
        answer_id=Utils.get_random_number(5),
        quest_id=question2.quest_id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
    )
    answer3 = Answer(
        answer_id=Utils.get_random_number(5),
        quest_id=question1.quest_id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
    )
    add_user(user)
    add_question(question1)
    add_question(question2)
    add_question(question3)
    add_answer(answer1)
    add_answer(answer2)
    add_answer(answer3)
    question = get_next_test(user.tg_user_id)
    assert question.quest_id == question3.quest_id
    remove_questions(Specialty.FOR_TEST.value)
    remove_user(user)


def test_get_test_result():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.FOR_TEST.value,
    )
    question = Question(
        quest_id=Utils.get_random_number(5),
        question_type=Specialty.FOR_TEST.value,
        text_answer=Utils.get_random_text(10),
    )
    add_user(user)
    add_question(question)
    question = get_next_test(user.tg_user_id)
    answer = get_test_result(user.tg_user_id)
    assert answer == question.text_answer
    remove_questions(Specialty.FOR_TEST.value)
    remove_user(user)
