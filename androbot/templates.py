from .config import settings
from .errors import TemplateNotFound


def render_message(template_text: str, **kwargs):
    """
    Функция заменяет параметры в шаблоне текста на реальные значения
    """
    parsed_text = template_text.strip().format(**kwargs)
    return parsed_text


def get_template(template_name: str) -> str:
    """
    Функция получет имя шаблона и возвращает содержимое этого файла.
    Если передать имя файла без расширения md - то оно добавиться
    """
    template_file = settings.static_folder / template_name
    if not template_file.exists() and template_file.suffix != ".md":
        template_file = template_file.with_suffix(".md")
        from loguru import logger

        logger.error(template_file)
        if not template_file.exists():
            raise TemplateNotFound(f"Template {template_name} not found!")

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    return answer_text
