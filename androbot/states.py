from aiogram.utils.helper import Helper, HelperMode, ListItem


class MainDialogueStates(Helper):
    """
    Состояния бота в режиме конечных автоматов, в главном меню
    """

    mode = HelperMode.snake_case

    MAIN_MENU = ListItem()
    IN_PROFILE = ListItem()
    DO_YOU_WANT_TO_CONTINUE_TEST = ListItem()
    FIRST_QUESTION = ListItem()
