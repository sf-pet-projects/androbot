import argparse
import os

from androbot import models
from androbot.actions import Actions
from androbot.database import engine
from androbot.types_ import Specialty


def load_questions(speciality: Specialty, filename: str, drop_questions: bool) -> None:
    models.Base.metadata.create_all(bind=engine)

    with Actions() as act:

        if drop_questions:
            act.remove_questions(speciality.value)

        act.load_questions(specialty=speciality, file=filename)


def main():
    all_specialities = [s.value for s in Specialty]
    default_speciality = Specialty.ANDROID

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="csv file with questions", type=str)
    parser.add_argument(
        "-s",
        "--speciality",
        help=f"choose speciality from {all_specialities} ",
        type=str,
        default=default_speciality,
    )
    parser.add_argument(
        "-d", "--drop_questions", help="drop questions before load", action="store_true"
    )
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f"File '{args.filename}' doesn't exist")
        return

    try:
        speciality = Specialty(args.speciality)
    except ValueError:
        print(f"Wrong speciality '{args.speciality}")
        return

    load_questions(speciality, args.filename, args.drop_questions)


if __name__ == "__main__":
    main()
