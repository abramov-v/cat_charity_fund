# Благотворительный фонд поддержки - QRKot

## О проекте
Асинхронное приложение на FastAPI для управления благотворительными проектами и пожертвованиями.  
Пользователи могут делать пожертвования, а суперпользователи — создавать и редактировать проекты.  
Все средства автоматически распределяются между открытыми проектами.

## Возможности
- Регистрация и аутентификация пользователей (JWT).
- Управление проектами (CRUD, доступно только суперпользователям).
- Создание пожертвований (для авторизованных пользователей).
- Автоматическое распределение пожертвований по проектам.
- Swagger-документация доступна по адресу `/docs`.


## Используемый стек
```
Python 3.10+
FastAPI
Pydantic
SQLAlchemy (async)
Alembic
Uvicorn
FastAPI Users
Pytest
Flake8
```

## Установка

1. Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone git@github.com:abramov-v/cat_charity_fund.git
cd cat_charity_fund
```

2. Создайте и активируйте виртуальное окружение:
   
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4.  Настройте переменные окружения:

Скопируйте файл `.env.example` и создайте на его основе `.env`:

```bash
cp .env.example .env
```

Пример содержимого .env:

```env
APP_TITLE=Благотворительный фонд поддержки котиков - QRKot
APP_DESC=Приложение для управления благотворительными проектами
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET_KEY=your_super_secret_key_here
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=your_strong_password_here
```

5. Инициализируйте базу данных и выполните миграции:

```bash
alembic upgrade head
```

Если вы вносите изменения в модели и хотите создать новую миграцию, выполните:

```bash
alembic revision --autogenerate -m "Комментарий к миграции"
alembic upgrade head
```

6. Запустите приложение:

```bash
uvicorn app.main:app --reload
```

После запуска приложение будет доступно по адресам:

Swagger UI: `http://127.0.0.1:8000/docs`
ReDoc: `http://127.0.0.1:8000/redoc`



## Примеры запросов к API 
Подробные варианты запросов и ошибок описаны в [`openapi.yml`](./openapi.yml).  
Ниже приведены базовые примеры.


### Аутентификация

**Логин (получение JWT):**

```http
POST /auth/jwt/login
Content-Type: application/x-www-form-urlencoded
```

```username=admin@example.com&password=secret```

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJh...",
  "token_type": "bearer"
}
```

**Регистрация нового пользователя**

```http
POST /auth/register
Content-Type: application/json
```

```json
{
  "email": "user@example.com",
  "password": "123456"
}
```

### Работа с проектами


**Получить все проекты:**

```http
GET /charity_project/
```

```json
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2019-08-24T14:15:22Z",
    "close_date": "2019-08-24T14:15:22Z"
  }
]
```


**Создать проект (только суперпользователь):**

```http
POST /charity_project/
Authorization: Bearer <token>
Content-Type: application/json
```

Тело запроса:

```json
{
  "name": "string",
  "description": "string",
  "full_amount": 0
}
```json

Тело ответа:

```json
{
  "name": "string",
  "description": "string",
  "full_amount": 0,
  "id": 0,
  "invested_amount": 0,
  "fully_invested": true,
  "create_date": "2019-08-24T14:15:22Z",
  "close_date": "2019-08-24T14:15:22Z"
}
```

### Работа с пожертвованиями

** Сделать пожертвование:**

```http
POST /donation/
Authorization: Bearer <token>
Content-Type: application/json
```

Тело запроса:

```json
{
  "full_amount": 500,
  "comment": "На корм котикам"
}
```

Тело ответа:

```json
{
  "full_amount": 0,
  "comment": "string",
  "id": 0,
  "create_date": "2019-08-24T14:15:22Z"
}
```


## Автор
**Валерий Абрамов**
- GitHub: [@abramov-v](https://github.com/abramov-v)
