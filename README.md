# Book API

REST API для управления коллекцией книг, построенный с использованием FastAPI и SQLite.

## Технологии

- FastAPI
- SQLAlchemy
- SQLite
- Docker

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd book-api
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
.\venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
cd app
uvicorn main:app --reload
```

### Запуск через Docker

1. Соберите Docker-образ:
```bash
docker build -t book-api .
```

2. Запустите контейнер:
```bash
docker run -d -p 8080:8080 --name book-api-container book-api
```

## API Endpoints

- `GET /books` - получить список всех книг
- `GET /books/{book_id}` - получить книгу по ID
- `POST /books` - создать новую книгу
- `PUT /books/{book_id}` - обновить существующую книгу
- `DELETE /books/{book_id}` - удалить книгу

## Документация API

После запуска приложения, документация доступна по следующим URL:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc
- OpenAPI JSON: http://localhost:8080/openapi.json 