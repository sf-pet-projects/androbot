import argparse
import os

from androbot import models
from androbot.actions import Actions
from androbot.database import engine
from androbot.types_ import Specialty


def load_questions(speciality: Specialty, filename: str, drop_questions: bool) -> None:
    """
    Загружаем в базу данных вопросы из указанного csv файла.
    Указываем специальность для которой нужно загрузить вопросы
    Если указан параметр drop_questions - то удаляем старые
    вопросы перед загрузкой (если нет еще ответов - сработает)
    """

    models.Base.metadata.create_all(bind=engine)

    with Actions() as act:

        if drop_questions:
            act.remove_questions(speciality.value)

        act.load_questions(specialty=speciality, file=filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="csv file with questions", type=str)
    parser.add_argument(
        "-s",
        "--speciality",
        choices=[s.value for s in Specialty],
        default=Specialty.ANDROID,
    )
    parser.add_argument("-d", "--drop_questions", help="drop questions before load", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f"File '{args.filename}' doesn't exist")
        return

    speciality = Specialty(args.speciality)

    load_questions(speciality, args.filename, args.drop_questions)


if __name__ == "__main__":
    main()
