# Бот для тестирование андройд разработчиков

Данный репозиторий призван помочь студентам из skillfactory подготовить к собеседованию на junior android developer.

**Установка**  

Требуется установка [poetry](https://github.com/python-poetry/poetry) в системе.  

```
git clone https://github.com/sf-pet-projects/androbot
cd androbot
poetry install
```


**Запуск**  

В переменной окружения ```TG_API_TOKEN``` надо проставить API токен бота.

```
poetry run python3 androbot/__init__.py
```

**Запуск в docker**

Перед запуском в докере требуется запустить `poetry install` (чтобы создался `poetry.lock` файл). А также создать `.env` файл с указанием `TG_API_TOKEN`.
```
docker build -t androbot -f docker/Dockerfile .
docker run --env-file .env --name androbot -d androbot
```

Войти в работающий контейнер
```
docker attach androbot          # подключиться к приложению
docker exec -ti androbot bash   # войти в bash
```
