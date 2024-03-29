import datetime

import pytest
from dateutil import tz

from androbot.actions import Actions, get_main_menu, start_new_test
from androbot.errors import NoNewQuestionsException, UserExistsException, UserNotExistsException, WrongBotScoreFormat
from androbot.schemas import Answer, EventsLog, Question, TelegramUser
from androbot.types_ import AnswerTypes, Events, Specialty
from androbot.types_.user_score import UserScore
from androbot.utils import Utils


@pytest.fixture()
def act():
    action = Actions()
    yield action
    action.__close__()


def test_get_main_menu():
    assert get_main_menu() == ["Android Developer"]


def test_start_new_test():
    assert start_new_test() == [
        AnswerTypes.VOICE.value,
        AnswerTypes.TEXT.value,
    ]


def test_add_user(act):
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    db_user = act.add_user(user)
    assert db_user.tg_user_id == user.tg_user_id
    act.remove_user(db_user)


def test_add_user_with_symbols_in_username(act):
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username="\"AL'🖐",
        specialty=Specialty.ANDROID.value,
    )
    db_user = act.add_user(user)
    assert db_user.tg_user_id == user.tg_user_id
    act.remove_user(db_user)


def test_add_already_exist_user(act):
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    act.add_user(user)
    with pytest.raises(UserExistsException):
        act.add_user(user)
    act.remove_user(user)


def test_remove_not_exist_user(act):
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    with pytest.raises(UserNotExistsException):
        act.remove_user(user)


def test_get_next_test(act):
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
    act.add_user(user)
    act.add_question(question1)
    act.add_question(question2)
    act.add_question(question3)
    act.get_next_test(user.tg_user_id)
    session = act.get_current_session(user.tg_user_id)
    assert session is not None
    answer1 = Answer(
        quest_id=question1.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
        session_id=session.id,
    )
    answer2 = Answer(
        quest_id=question2.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
        session_id=session.id,
    )
    answer3 = Answer(
        quest_id=question1.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
        session_id=session.id,
    )
    act.add_answer(answer1)
    act.add_answer(answer2)
    act.add_answer(answer3)
    question = act.get_next_test(user.tg_user_id)[0]
    assert question.id == question3.id
    act.remove_user(user)
    act.remove_questions("test")


def test_get_current_question(act):
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
    act.add_user(user)
    act.add_question(question)
    question = act.get_next_test(user.tg_user_id)[0]
    right_answer = act.get_current_question(user.tg_user_id).text_answer
    assert right_answer == question.text_answer
    act.remove_user(user)
    act.remove_questions("test")


def test_add_event(act):
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    act.add_user(user)
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
    act.add_event(event)
    act.remove_user(user)


def test_no_add_answer_with_empty_text(act):
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
    act.add_user(user)
    act.add_question(question1)
    act.add_question(question2)
    act.add_question(question3)
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
    assert act.add_answer(answer1) is not None
    assert act.add_answer(answer2) is None
    act.remove_user(user)
    act.remove_questions("test")


def test_has_started_test(act):
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
    act.add_user(user)
    assert act.has_started_test(user.tg_user_id) is False
    act.add_question(question)
    act.get_next_test(user.tg_user_id)
    assert act.has_started_test(user.tg_user_id) is True
    answer = Answer(
        quest_id=question.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer="   ",
        link_to_audio_answer=Utils.get_random_text(50),
    )
    act.add_answer(answer)
    with pytest.raises(NoNewQuestionsException):
        act.get_next_test(user.tg_user_id)
    act.remove_user(user)
    act.remove_questions("test")


def test_start_test_after_reset_session(act):
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

    act.add_user(user)
    assert act.has_started_test(user.tg_user_id) is False
    act.add_question(question)
    answer = Answer(
        quest_id=question.id,
        tg_user_id=user.tg_user_id,
        answer_type=start_new_test()[1],
        text_answer=Utils.get_random_text(50),
        link_to_audio_answer=Utils.get_random_text(50),
    )
    act.add_answer(answer)
    act.reset_session(user)
    assert act.get_next_test(user.tg_user_id)[0].text_question == question.text_question
    act.remove_user(user)
    act.remove_questions("test")


def test_add_bot_score(act):
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    act.add_user(user)
    act.add_bot_score(user, 5)
    assert act.get_bot_review(user)[0].bot_score == 5
    act.add_bot_score(user, 3)
    assert act.get_bot_review(user)[0].bot_score == 3
    with pytest.raises(WrongBotScoreFormat):
        act.add_bot_score(user, 15)


def test_add_bot_review(act):
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    my_review = "Some review"
    my_other_review = "Some new review"
    act.add_user(user)
    act.add_bot_review(user, my_review, AnswerTypes.VOICE)
    assert act.get_bot_review(user)[0].bot_review == my_review
    act.add_bot_review(user, my_other_review, AnswerTypes.TEXT)
    assert act.get_bot_review(user)[1].bot_review == my_other_review
    assert act.get_bot_review(user)[1].bot_review_type == AnswerTypes.TEXT.name


def test_add_problem_question_review(act):
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
    review = "Описание проблемы"
    second_review = "Второе описание проблемы"
    act.add_user(user)
    act.add_question(question)
    act.add_problem_question_review(question.id, user.tg_user_id, review, AnswerTypes.TEXT)
    assert act.get_problem_question_review(user.tg_user_id)[0].review == review
    act.add_problem_question_review(question.id, user.tg_user_id, second_review, AnswerTypes.VOICE)
    assert act.get_problem_question_review(user.tg_user_id)[1].review == second_review
    act.remove_problem_question_review(user.tg_user_id, question.id)
    act.remove_user(user)
    act.remove_questions("test")


def test_add_question_score(act):
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
    act.add_user(user)
    act.add_question(question)
    act.add_question_score(question.id, user.tg_user_id, UserScore.PARTLY.value)
    assert act.get_question_score(question.id, user.tg_user_id)[0].score == UserScore.PARTLY.value
    act.add_question_score(question.id, user.tg_user_id, UserScore.RIGHT.value)
    assert act.get_question_score(question.id, user.tg_user_id)[1].score == UserScore.RIGHT.value
    act.remove_question_score(question.id)
    act.remove_user(user)
    act.remove_questions("test")


def test_add_train_material(act):
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
    act.add_user(user)
    act.add_question(question)
    act.add_train_material(question.id, user.tg_user_id)
    assert act.get_train_material(user.tg_user_id)[0].tg_user_id == user.tg_user_id
    act.remove_train_material(user.tg_user_id, question.id)
    act.remove_user(user)
    act.remove_questions("test")
