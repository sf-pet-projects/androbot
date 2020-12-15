from aiogram.dispatcher.filters.state import State, StatesGroup


class DialogueStates(StatesGroup):
    """
    Состояния бота в режиме конечных автоматов, в главном меню
    """

    MAIN_MENU = State()
    ANDROID_DEVELOPER_INIT_VIEW = State()
    SELECT_ANSWER_TYPE = State()
    ASK_QUESTION = State()
    CALL_TO_SEND_ANSWER = State()
    GOT_ANSWER = State()
    DO_NOT_UNDERSTAND_1 = State()
    DO_NOT_UNDERSTAND_2 = State()
    NO_NEW_QUESTIONS = State()
