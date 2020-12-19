# Бот для тестирование андройд разработчиков

Данный репозиторий призван помочь студентам из skillfactory подготовить к собеседованию на junior android developer.

**Установка**  

Требуется установка [`poetry`](https://github.com/python-poetry/poetry) в системе.  

```
git clone https://github.com/sf-pet-projects/androbot
cd androbot
poetry install
```

**Использование pre-commit**  

В проекте используются:
 - [`isort`](https://pycqa.github.io/isort/)
 - [`black`](https://black.readthedocs.io/en/stable/)
 - [`flake8`](https://flake8.pycqa.org/en/latest/)
 - [`mypy`](http://mypy-lang.org/)
 
Они помогают нам делать код чище, проверяют его на соблюдение стандартов.

`poetry run pre-commit install` установить git hooks, которые будут запускать проверки перед каждым коммитом, сделают исправления или не дадут закоммитить, если код не пройдет првоерку.

Также можно вручную запустить проверку и исправление. Для этого нужно добавить в stage необходимые файлы, и выполнить pre-commit

```
git add andobot/main.py
poetry run pre-commit
```

**Указание переменных окружения**

`cp .env_example .env` - инициализация файла `.env`

Заполните в нем следующие параметры:
- `TG_API_TOKEN` - API токен бота [как его получить](https://habr.com/ru/post/262247/).    


**Инициализация базы данных**  

Перед первым запуском нужно загрузить вопросы в бота. Это делается с помощью команды:
```
poerty run python3 androbot\load_questions.py path_to_csv_file_with_questions.csv
```


**Запуск**  

```
poetry run python3 androbot/__init__.py
```

**Запуск в docker**

Перед запуском в докере требуется запустить `poetry install` (чтобы создался `poetry.lock` файл).
```
docker build -t androbot -f docker/Dockerfile .
docker run --env-file .env --name androbot -d androbot
```

Войти в работающий контейнер
```
docker attach androbot          # подключиться к приложению
docker exec -ti androbot bash   # войти в bash
```

**Запуск тестов**

```
pytest androbot/tests.py
```
