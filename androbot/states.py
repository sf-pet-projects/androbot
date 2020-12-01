from aiogram.utils.helper import Helper, HelperMode, ListItem


class DialogueStates(Helper):
    """
    Состояния бота в режиме конечных автоматов, в главном меню
    """

    mode = HelperMode.snake_case

    MAIN_MENU = ListItem()
    ANDROID_DEVELOPER_INIT_VIEW = ListItem()
    FIRST_QUESTION = ListItem()
