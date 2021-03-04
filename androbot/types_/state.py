from aiogram.dispatcher.filters.state import State, StatesGroup


class DialogueStates(StatesGroup):
    """
    Состояния бота в режиме конечных автоматов, в главном меню
    """

    MAIN_MENU = State()
    HAS_STARTED_TEST = State()
    SELECT_ANSWER_TYPE = State()
    ARE_YOU_READY_FOR_TEST = State()
    ASK_QUESTION = State()
    GOT_ANSWER = State()
    DO_NOT_UNDERSTAND_1 = State()
    DO_NOT_UNDERSTAND_2 = State()
    NO_NEW_QUESTIONS = State()
