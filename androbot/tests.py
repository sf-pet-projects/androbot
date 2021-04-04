import datetime

import pytest
from dateutil import tz

from androbot.actions import Actions, get_main_menu, start_new_test
from androbot.errors import NoNewQuestionsException, UserExistsException, UserNotExistsException, WrongBotScoreFormat
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
    try:
        with Actions() as act:
            db_user = act.add_user(user)
            assert db_user.tg_user_id == user.tg_user_id
    finally:
        act.remove_user(db_user)


def test_add_user_with_symbols_in_username():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username="\"AL'🖐",
        specialty=Specialty.ANDROID.value,
    )
    try:
        with Actions() as act:
            db_user = act.add_user(user)
            assert db_user.tg_user_id == user.tg_user_id
    finally:
        act.remove_user(db_user)


def test_add_already_exist_user():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty=Specialty.ANDROID.value,
    )
    try:
        with Actions() as act:
            act.add_user(user)
            with pytest.raises(UserExistsException):
                act.add_user(user)
    finally:
        act.remove_user(user)


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
    with Actions() as act:
        act.add_user(user)
        act.add_question(question1)
        act.add_question(question2)
        act.add_question(question3)
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
        try:
            act.add_answer(answer1)
            act.add_answer(answer2)
            act.add_answer(answer3)
            question = act.get_next_test(user.tg_user_id)
            assert question.id == question3.id
        finally:
            act.remove_user(user)
            act.remove_questions("test")


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
    try:
        with Actions() as act:
            act.add_user(user)
            act.add_question(question)
            question = act.get_next_test(user.tg_user_id)
            right_answer = act.get_current_question(user.tg_user_id).text_answer
            assert right_answer == question.text_answer
    finally:
        act.remove_user(user)
        act.remove_questions("test")


def test_add_event():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    try:
        with Actions() as act:
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
    finally:
        act.add_event(event)
        act.remove_user(user)


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
    try:
        with Actions() as act:
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
    finally:
        act.remove_user(user)
        act.remove_questions("test")


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
    try:
        with Actions() as act:
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
    finally:
        act.remove_user(user)
        act.remove_questions("test")


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
    try:
        with Actions() as act:
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
            assert act.get_next_test(user.tg_user_id).text_question == question.text_question
    finally:
        act.remove_user(user)
        act.remove_questions("test")


def test_add_bot_score():
    user = TelegramUser(
        tg_user_id=Utils.get_random_number(5),
        name=Utils.get_random_text(10),
        username=Utils.get_random_text(10),
        specialty="test",
    )
    with Actions() as act:
        act.add_user(user)
        act.add_bot_score(user, 5)
        assert act.get_bot_review(user).bot_score == 5
        act.add_bot_score(user, 3)
        assert act.get_bot_review(user).bot_score == 3
        with pytest.raises(WrongBotScoreFormat):
            act.add_bot_score(user, 15)


def test_add_problem_question_review():
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
    try:
        with Actions() as act:
            act.add_user(user)
            act.add_question(question)
            act.add_problem_question_review(question.id, user.tg_user_id, review, AnswerTypes.TEXT)
            assert act.get_problem_question_review(user.tg_user_id)[0].review == review
            act.add_problem_question_review(question.id, user.tg_user_id, second_review, AnswerTypes.VOICE)
            assert act.get_problem_question_review(user.tg_user_id)[1].review == second_review
    finally:
        act.remove_problem_question_review(user.tg_user_id, question.id)
        act.remove_user(user)
        act.remove_questions("test")


def test_add_question_score():
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
    try:
        with Actions() as act:
            act.add_user(user)
            act.add_question(question)
            act.add_question_score(question.id, user.tg_user_id, False)
            assert act.get_question_score(question.id, user.tg_user_id)[0].is_correct is False
            act.add_question_score(question.id, user.tg_user_id, True)
            assert act.get_question_score(question.id, user.tg_user_id)[1].is_correct is True
    finally:
        act.remove_question_score(user.tg_user_id, question.id)
        act.remove_user(user)
        act.remove_questions("test")


def test_add_train_material():
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
    try:
        with Actions() as act:
            act.add_user(user)
            act.add_question(question)
            act.add_train_material(question.id, user.tg_user_id)
            assert act.get_train_material(user.tg_user_id)[0].tg_user_id == user.tg_user_id
    finally:
        act.remove_train_material(user.tg_user_id, question.id)
        act.remove_user(user)
        act.remove_questions("test")
