import aiogram.types as aiotypes


def render_message(template_text: str, message: aiotypes.Message):
    """
    Функция заменяет параметры в шаблоне текста на реальные значения
    """
    values = dict(username=message.from_user.username)
    parsed_text = template_text.format(**values)
    return parsed_text
