import datetime
import pytest

from dateutil import tz

from androbot.actions import Actions, get_main_menu, start_new_test
from androbot.errors import NoNewQuestionsException, UserExistsException, UserNotExistsException
from androbot.schemas import Answer, EventsLog, Question, TelegramUser
from androbot.types_ import AnswerTypes, Events, Specialty
from androbot.utils import Utils


def test_get_main_menu():
    assert get_main_menu() == ["Android Developer"]


def test_start_new_test():
    assert start_new_test() == [
        AnswerTypes.VOICE.value,
        AnswerTypes.TEXT.value,
    ]


def test_add_user():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    db_user = Actions().add_user(user)
    assert db_user.tg_user_id == user.tg_user_id
    Actions().remove_user(db_user)


def test_add_user_with_symbols_in_username():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username="\"AL'🖐",
        specialty=Specialty.ANDROID.value,
    )
    db_user = Actions().add_user(user)
    assert db_user.tg_user_id == user.tg_user_id
    Actions().remove_user(db_user)


def test_add_already_exist_user():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    Actions().add_user(user)
    with pytest.raises(UserExistsException):
        Actions().add_user(user)
    Actions().remove_user(user)


def test_remove_not_exist_user():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    with pytest.raises(UserNotExistsException):
        Actions().remove_user(user)


def test_get_next_test():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    question1 = Question(
        question_type="test",
        question_category=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        text_answer=Utils.get_random_text(10),
    )
    question2 = Question(
        question_type="test",
        question_category=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        text_answer=Utils.get_random_text(10),
    )
    question3 = Question(
        question_type="test",
        question_category=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        text_answer=Utils.get_random_text(10),
    )
    Actions().add_user(user)
    Actions().add_question(question1)
    Actions().add_question(question2)
    Actions().add_question(question3)
    answer1 = Answer(
        quest_id=question1.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
    )
    answer2 = Answer(
        quest_id=question2.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
    )
    answer3 = Answer(
        quest_id=question1.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
    )
    Actions().add_answer(answer1)
    Actions().add_answer(answer2)
    Actions().add_answer(answer3)
    question = Actions().get_next_test(user.tg_user_id)
    assert question.id == question3.id
    Actions().remove_user(user)
    Actions().remove_questions("test")


def test_get_current_question():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    question = Question(
        question_type="test",
        text_answer=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        additional_info=Utils.get_random_text(10),
    )
    Actions().add_user(user)
    Actions().add_question(question)
    question = Actions().get_next_test(user.tg_user_id)
    right_answer = Actions().get_current_question(user.tg_user_id).text_answer
    assert right_answer == question.text_answer
    Actions().remove_user(user)
    Actions().remove_questions("test")


def test_add_event():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    Actions().add_user(user)
    MSC = tz.gettz("Europe/Moscow")
    event = EventsLog(
        tg_user_id=user.tg_user_id,
        event_type=Events.SendSolution,
        datetime=datetime.datetime.now(tz=MSC),
        param1=Specialty.ANDROID.value,
        param2=Utils.get_random_number(5),
        param3=Utils.get_random_number(5),
        param4=AnswerTypes.VOICE.value,
    )
    Actions().add_event(event)
    Actions().remove_user(user)


def test_no_add_answer_with_empty_text():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    question1 = Question(
        question_type="test",
        question_category=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        text_answer=Utils.get_random_text(10),
    )
    question2 = Question(
        question_type="test",
        question_category=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        text_answer=Utils.get_random_text(10),
    )
    question3 = Question(
        question_type="test",
        question_category=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        text_answer=Utils.get_random_text(10),
    )
    Actions().add_user(user)
    Actions().add_question(question1)
    Actions().add_question(question2)
    Actions().add_question(question3)
    answer1 = Answer(
        quest_id=question1.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer="   ",
        link_to_audio_answer=Utils.get_random_text(50),
    )
    answer2 = Answer(
        quest_id=question2.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer="   ",
        link_to_audio_answer="",
    )
    assert Actions().add_answer(answer1) is not None
    assert Actions().add_answer(answer2) is None
    Actions().remove_user(user)
    Actions().remove_questions("test")


def test_has_started_test():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    question = Question(
        question_type="test",
        question_category=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        text_answer=Utils.get_random_text(10),
    )
    Actions().add_user(user)
    assert Actions().has_started_test(user.tg_user_id) is False
    Actions().add_question(question)
    Actions().get_next_test(user.tg_user_id)
    assert Actions().has_started_test(user.tg_user_id) is True
    answer = Answer(
        quest_id=question.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer="   ",
        link_to_audio_answer=Utils.get_random_text(50),
    )
    Actions().add_answer(answer)
    with pytest.raises(NoNewQuestionsException):
        Actions().get_next_test(user.tg_user_id)
    Actions().remove_user(user)
    Actions().remove_questions("test")


def test_start_test_after_reset_session():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    question = Question(
        question_type="test",
        question_category=Utils.get_random_text(10),
        text_question=Utils.get_random_text(10),
        text_answer=Utils.get_random_text(10),
    )
    Actions().add_user(user)
    assert Actions().has_started_test(user.tg_user_id) is False
    Actions().add_question(question)
    answer = Answer(
        quest_id=question.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
    )
    Actions().add_answer(answer)
    Actions().reset_session(user)
    assert Actions().get_next_test(user.tg_user_id).text_question == question.text_question
    Actions().remove_user(user)
    Actions().remove_questions("test")
