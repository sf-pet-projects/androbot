def render_message(template_text: str, **kwargs):
    """
    Функция заменяет параметры в шаблоне текста на реальные значения
    """
    parsed_text = template_text.strip().format(**kwargs)
    return parsed_text
