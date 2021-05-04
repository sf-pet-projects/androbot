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
    NO_ANSWER = State()
    ANSWER_SCORED_BY_USER = State()
    DO_NOT_UNDERSTAND = State()
    DO_YOU_WANT_GET_ANSWER = State()
    USER_SCORE = State()
    BOT_SCORE = State()
    BOT_REVIEW = State()
    FINISH = State()
