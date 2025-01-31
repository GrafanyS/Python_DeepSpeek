# paython + react сайт с авторизацией:
admin панелью, навигацией , admin панель с выдачей прав пользователям, заполнением таблиц динамических, данными. Таблицы добавляются из admin панели, названия колонок и количество задаются тоже. Авторизированным пользователям, разрешается вводить данные в таблицы с правами редактирование. Права на редактирование и чтение, только чтение. В admin панели. Удаление таблиц или пользователей только с правами adminstrator. Добавьте валидацию данных на фронтенде и бэкенде. Улучшите интерфейс с помощью Tailwind ( добавить анимацию). запуск в контейнере Docker, docker-compose.
Создание веб-приложения с использованием Python (Django) и React, с авторизацией, административной панелью, динамическими таблицами и правами доступа, требует нескольких шагов. Ниже приведен пример реализации такого проекта с использованием Docker и Docker Compose.

## 1. Структура проекта
```bash
project/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── backend/
│       ├── settings.py
│       ├── urls.py
│       ├── models.py
│       └── views.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.js
│   │   └── index.js
│   └── public/
├── docker-compose.yml
└── README.md
```
## 2. Backend (Django)
Установка зависимостей
Создайте файл `requirements.txt` в папке backend:

```bash
Django==4.2
djangorestframework==3.14.0
django-cors-headers==4.2.0
psycopg2-binary==2.9.6
```
### Настройка Django
Создайте Django-проект:

```bash
django-admin startproject backend
```
В `settings.py` добавьте настройки для CORS, REST Framework и базы данных:

```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```
### Создайте модели для пользователей, таблиц и прав доступа в `models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class DynamicTable(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class TableColumn(models.Model):
    table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50)

class TableRow(models.Model):
    table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)
    data = models.JSONField()

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
```

### Создайте API для работы с таблицами и пользователями в `views.py`:

```python
from rest_framework import viewsets, permissions
from .models import DynamicTable, TableColumn, TableRow, UserPermission
from .serializers import DynamicTableSerializer, TableColumnSerializer, TableRowSerializer, UserPermissionSerializer

class DynamicTableViewSet(viewsets.ModelViewSet):
    queryset = DynamicTable.objects.all()
    serializer_class = DynamicTableSerializer
    permission_classes = [permissions.IsAuthenticated]

class TableColumnViewSet(viewsets.ModelViewSet):
    queryset = TableColumn.objects.all()
    serializer_class = TableColumnSerializer
    permission_classes = [permissions.IsAuthenticated]

class TableRowViewSet(viewsets.ModelViewSet):
    queryset = TableRow.objects.all()
    serializer_class = TableRowSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAdminUser]
```

### Настройте маршруты в `urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DynamicTableViewSet, TableColumnViewSet, TableRowViewSet, UserPermissionViewSet

router = DefaultRouter()
router.register(r'tables', DynamicTableViewSet)
router.register(r'columns', TableColumnViewSet)
router.register(r'rows', TableRowViewSet)
router.register(r'permissions', UserPermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

## 3. Frontend (React)
Установка зависимостей
Создайте файл `package.json` в папке frontend:

```json
{
  "name": "frontend",
  "version": "1.0.0",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.2",
    "axios": "^1.5.0",
    "tailwindcss": "^3.3.3"
  }
}
```
### Настройка Tailwind
Установите Tailwind:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```
### Настройте `tailwind.config.js`:

```javascript
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```
### Добавьте Tailwind в `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```
### Создание компонентов
Создайте компоненты для авторизации, таблиц и административной панели.

Используйте Axios для взаимодействия с бэкендом.

## 4. Docker и Docker Compose
### Dockerfile для Backend
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```
### Dockerfile для Frontend
```dockerfile
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["npm", "start"]
```
#### docker-compose.yml
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```
## 5. Запуск проекта
Соберите и запустите контейнеры:

```bash
docker-compose up --build
```
Откройте браузер и перейдите по адресу http://localhost:3000.

##  6. Дополнительные улучшения
Добавьте анимации с помощью Tailwind (например, animate-pulse, animate-bounce).

Реализуйте валидацию данных на фронтенде с помощью библиотеки yup или zod.

Настройте CI/CD для автоматического развертывания.

Этот проект можно расширять и улучшать в зависимости от ваших требований.

## Настройте CI/CD для автоматического развертывания github
Настройка CI/CD для автоматического развертывания вашего проекта с использованием GitHub Actions включает в себя создание рабочего процесса (workflow), который будет автоматически собирать, тестировать и развертывать ваше приложение при каждом изменении в репозитории (например, при пуше в ветку main).

Ниже приведен пример настройки CI/CD для вашего проекта (Python + React) с использованием GitHub Actions.

1. Создание файла GitHub Actions
В корне вашего репозитория создайте папку .github/workflows.

Внутри этой папки создайте файл `ci-cd.yml`.

2. Пример файла `ci-cd.yml`
```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main  # Запускать только при пуше в ветку main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      # Шаг 1: Проверка кода
      - name: Checkout code
        uses: actions/checkout@v3

      # Шаг 2: Настройка Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      # Шаг 3: Логин в Docker Hub (если вы используете Docker Hub для хранения образов)
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_TOKEN }}

      # Шаг 4: Сборка и публикация образов
      - name: Build and push backend image
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: your-dockerhub-username/backend:latest

      - name: Build and push frontend image
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          push: true
          tags: your-dockerhub-username/frontend:latest

      # Шаг 5: Развертывание на сервере (например, через SSH)
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            docker-compose down
            docker-compose pull
            docker-compose up -d
```
### 3. Настройка секретов в GitHub
Для работы CI/CD вам нужно добавить секреты в настройках вашего репозитория на GitHub:

Перейдите в Settings -> Secrets and variables -> Actions.

Добавьте следующие секреты:

DOCKER_HUB_USERNAME — ваш логин на Docker Hub.

DOCKER_HUB_TOKEN — ваш токен Docker Hub (можно получить в настройках аккаунта Docker Hub).

SSH_HOST — IP-адрес или домен вашего сервера.

SSH_USERNAME — имя пользователя для SSH.

SSH_PRIVATE_KEY — приватный SSH-ключ для доступа к серверу.

### 4. Настройка сервера для развертывания
Убедитесь, что на вашем сервере установлены Docker и Docker Compose.

Скопируйте файл `docker-compose.yml` на сервер.

Убедитесь, что сервер доступен по SSH.

### 5. Как это работает
При каждом пуше в ветку main GitHub Actions запускает рабочий процесс.

Сначала собираются Docker-образы для backend и frontend.

Образы публикуются в Docker Hub.

Затем происходит подключение к серверу по SSH и выполнение команд для обновления контейнеров:

Остановка текущих контейнеров (docker-compose down).

Загрузка новых образов (docker-compose pull).

Запуск обновленных контейнеров (docker-compose up -d).

### 6. Дополнительные улучшения
Тестирование: Добавьте шаги для запуска тестов (например, unit-тесты для Python и React).

Уведомления: Настройте уведомления в Slack или Telegram при успешном или неудачном завершении CI/CD.

Окружения: Используйте разные окружения (например, staging и production) для тестирования и продакшена.

### 7. Пример с тестами
Добавьте шаги для тестирования в `ci-cd.yml`:

```yaml
- name: Run backend tests
  run: |
    cd backend
    python manage.py test

- name: Run frontend tests
  run: |
    cd frontend
    npm test
```
Теперь ваш проект будет автоматически развертываться при каждом изменении в ветке main. Это значительно упрощает процесс разработки и deployment.
