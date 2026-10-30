# LMS API — FastAPI + SQLite + SQLAlchemy

Небольшое REST API системы управления обучением (LMS), созданное для университетской лабораторной работы.
Оно полностью запускается локально, чтобы товарищ по команде мог склонировать его и протестировать эндпоинты через Postman.

## Требования

- Python **3.10.12** (или любая версия 3.10+)
- `pip`

## Установка и запуск

```bash
# 1. Создать и активировать виртуальное окружение
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить сервер
uvicorn app.main:app --reload
```

Сервер доступен по адресу **http://127.0.0.1:8000**.

- Интерактивная документация API (Swagger UI): **http://127.0.0.1:8000/docs**
- OpenAPI схема: **http://127.0.0.1:8000/openapi.json**

> Файл `db.sqlite3` **закоммичен** в этом репозитории и уже заполнен тестовыми
> данными, поэтому ручная настройка базы данных не требуется. При первом запуске
> приложение создаёт таблицы (если их нет) и наполняет данными только когда база
> данных пуста.

## Эндпоинты (всего 8)

| # | Метод | Путь | Параметры | Тело |
|---|--------|------|--------|------|
| 1 | GET | `/courses` | query: `search`, `category_id`, `teacher_id` | — |
| 2 | POST | `/courses` | — | `title`, `description`, `teacher_id`, `category_id` |
| 3 | PUT | `/courses/{course_id}` | path | любые из: `title`, `description`, `teacher_id`, `category_id` |
| 4 | DELETE | `/courses/{course_id}` | path | — (каскадное удаление lessons/enrollments/assignments/submissions) |
| 5 | GET | `/lessons` | query: `course_id` | — |
| 6 | POST | `/enrollments` | — | `user_id`, `course_id` |
| 7 | POST | `/submissions` | — | `assignment_id`, `user_id`, `content` |
| 8 | PUT | `/submissions/{submission_id}` | path | `score?`, `status?` |

## Тестовые данные (seed)

Эти идентификаторы доступны «из коробки» для тестирования:

- **Категории**: `1` Programming, `2` Mathematics, `3` Design
- **Пользователи**: `1` Alice Teacher (teacher), `2` Bob Student (student),
  `3` Carol Student (student), `4` Admin User (admin)
- **Курсы**: `1` Python Basics, `2` Linear Algebra
- **Уроки**: `1` и `2` для курса 1, `3` для курса 2
- **Задания**: `1` (курс 1)
- **Записи на курс**: Bob (`2`) → курс `1`
- **Сдачи заданий**: `1` (задание `1`, от Bob, статус `pending`)

### Примеры запросов (Postman / curl)

```bash
# Получить список курсов, отфильтровать по поисковому слову
curl "http://127.0.0.1:8000/courses?search=Python"

# Создать курс (преподаватель 1, категория 1)
curl -X POST "http://127.0.0.1:8000/courses" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Course","description":"desc","teacher_id":1,"category_id":1}'

# Обновить курс
curl -X PUT "http://127.0.0.1:8000/courses/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'

# Удалить курс (каскадно)
curl -X DELETE "http://127.0.0.1:8000/courses/2"

# Получить список уроков курса
curl "http://127.0.0.1:8000/lessons?course_id=1"

# Записать студента на курс
curl -X POST "http://127.0.0.1:8000/enrollments" \
  -H "Content-Type: application/json" \
  -d '{"user_id":3,"course_id":2}'

# Сдать задание
curl -X POST "http://127.0.0.1:8000/submissions" \
  -H "Content-Type: application/json" \
  -d '{"assignment_id":1,"user_id":3,"content":"my answer"}'

# Оценить сдачу задания
curl -X PUT "http://127.0.0.1:8000/submissions/1" \
  -H "Content-Type: application/json" \
  -d '{"score":90,"status":"graded"}'
```

## Запуск тестов

Функциональные тесты используют `pytest` с временной базой `test.db` (отдельной от
закоммиченной `db.sqlite3`).

```bash
pip install -r requirements.txt   # уже выполнено выше
pytest                            # запускает tests/ на свежей тестовой БД
```

## Структура проекта

```
app/
  database.py   # engine, Base, SessionLocal, get_db, PRAGMA foreign_keys=ON, init_db()
  models.py     # 7 ORM-таблиц с каскадными связями
  schemas.py    # Pydantic v2 модели запросов/ответов
  seed.py       # наполняет справочники и тестовые данные
  routes.py     # 8 эндпоинтов
  main.py       # FastAPI-приложение + lifespan (создание таблиц + seed при запуске)
tests/          # функциональные тесты pytest
db.sqlite3      # закоммиченная, заполненная база данных
requirements.txt
README.md
```
