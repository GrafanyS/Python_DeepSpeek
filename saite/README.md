# сайт

сайт с авторизацией, admin панель с выдачей прав пользователям, заполнением таблиц динамических, данными. Таблицы добавляются из admin панели, названия колонок и количество задаются тоже. Авторизированным пользователям, разрешается вводить данные в таблицы с правами редактирование. Права на редактирование и чтение, только чтение. В admin панели. Удаление таблиц или пользователей только с правами adminstrator. Добавьте валидацию данных на фронтенде и бэкенде. Улучшите интерфейс с помощью Tailwind ( добавить анимацию). запуск в контейнере Docker, docker-compose.
Для реализации описанного вами проекта, потребуется несколько шагов. Мы создадим веб-приложение с авторизацией, административной панелью, динамическими таблицами и правами доступа. В качестве стека технологий будем использовать:

* Frontend: React.js с Tailwind CSS для стилизации и анимаций.

* Backend: Node.js с Express.js для обработки запросов и валидации данных.

D* atabase: PostgreSQL для хранения данных.

* Authentication: JWT (JSON Web Tokens) для авторизации.

* Docker: Для запуска приложения в контейнерах.

## 1. Структура проекта
```bash
project/
│
├── backend/
│   ├── Dockerfile
│   ├── src/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── utils/
│   │   └── index.js
│   └── package.json
│
├── frontend/
│   ├── Dockerfile
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── docker-compose.yml
└── README.md
```
### 2. Backend (Node.js + Express.js)

#### 2.1. Установка зависимостей
```bash
cd backend
npm init -y
npm install express pg sequelize jsonwebtoken bcryptjs cors
npm install --save-dev nodemon
```
#### 2.2. Настройка Express.js
```javascript
// backend/src/index.js
const express = require('express');
const cors = require('cors');
const sequelize = require('./utils/database');
const authRoutes = require('./routes/auth');
const adminRoutes = require('./routes/admin');
const tableRoutes = require('./routes/table');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/table', tableRoutes);

const PORT = process.env.PORT || 5000;

sequelize.sync().then(() => {
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
});
2.3. Модели Sequelize
javascript
Copy
// backend/src/models/user.js
const { DataTypes } = require('sequelize');
const sequelize = require('../utils/database');

const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  username: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  role: {
    type: DataTypes.ENUM('admin', 'editor', 'viewer'),
    defaultValue: 'viewer',
  },
});

module.exports = User;
2.4. Роуты и контроллеры
javascript
Copy
// backend/src/routes/auth.js
const express = require('express');
const { login, register } = require('../controllers/auth');

const router = express.Router();

router.post('/login', login);
router.post('/register', register);

module.exports = router;
javascript
Copy
// backend/src/controllers/auth.js
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { User } = require('../models/user');

const login = async (req, res) => {
  // Логика входа
};

const register = async (req, res) => {
  // Логика регистрации
};

module.exports = { login, register };
```
### 3. Frontend (React.js + Tailwind CSS)
#### 3.1. Установка зависимостей
```bash
cd frontend
npx create-react-app .
npm install axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
#### 3.2. Настройка Tailwind CSS
```javascript
// frontend/tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
css
Copy
/* frontend/src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
3.3. Компоненты и страницы
javascript
Copy
// frontend/src/components/Navbar.js
import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-blue-500 p-4 text-white">
      <div className="container mx-auto">
        <h1 className="text-xl font-bold">Admin Panel</h1>
      </div>
    </nav>
  );
};

export default Navbar;
```
### 4. Docker и Docker Compose
#### 4.1. Dockerfile для Backend
```Dockerfile
# backend/Dockerfile
FROM node:14

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

CMD ["npm", "start"]
```
#### 4.2. Dockerfile для Frontend
```Dockerfile
# frontend/Dockerfile
FROM node:14

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

CMD ["npm", "start"]
```
#### 4.3. docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      DB_HOST: db
      DB_USER: admin
      DB_PASSWORD: password
      DB_NAME: appdb

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```
### 5. Запуск проекта
```bash
docker-compose up --build
```
### 6. Валидация данных
#### 6.1. Валидация на бэкенде
Используйте библиотеку express-validator для валидации данных на сервере.

```bash
npm install express-validator
```
```javascript
// backend/src/routes/auth.js
const { body, validationResult } = require('express-validator');

router.post(
  '/register',
  [
    body('username').isLength({ min: 3 }),
    body('password').isLength({ min: 6 }),
  ],
  register
);
```
#### 6.2. Валидация на фронтенде
Используйте библиотеку formik и yup для валидации форм.

```bash
npm install formik yup
```
```javascript
// frontend/src/components/RegisterForm.js
import { useFormik } from 'formik';
import * as Yup from 'yup';

const RegisterForm = () => {
  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
    },
    validationSchema: Yup.object({
      username: Yup.string().min(3, 'Must be at least 3 characters').required('Required'),
      password: Yup.string().min(6, 'Must be at least 6 characters').required('Required'),
    }),
    onSubmit: values => {
      // Отправка данных на сервер
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <input
        id="username"
        name="username"
        type="text"
        onChange={formik.handleChange}
        value={formik.values.username}
      />
      {formik.errors.username ? <div>{formik.errors.username}</div> : null}

      <input
        id="password"
        name="password"
        type="password"
        onChange={formik.handleChange}
        value={formik.values.password}
      />
      {formik.errors.password ? <div>{formik.errors.password}</div> : null}

      <button type="submit">Register</button>
    </form>
  );
};

export default RegisterForm;
7. Анимации с Tailwind CSS
javascript
Copy
// frontend/src/components/Table.js
import React from 'react';

const Table = () => {
  return (
    <div className="animate-fade-in">
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="px-6 py-3 border-b-2 border-gray-300 text-left text-sm leading-4 text-blue-500 tracking-wider">
              Column 1
            </th>
            <th className="px-6 py-3 border-b-2 border-gray-300 text-left text-sm leading-4 text-blue-500 tracking-wider">
              Column 2
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-500">
              Data 1
            </td>
            <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-500">
              Data 2
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default Table;
```
### Заключение
Этот проект представляет собой базовую структуру для создания веб-приложения с авторизацией, административной панелью и динамическими таблицами. Вы можете расширить его функциональность, добавив больше валидаций, улучшив интерфейс и добавив дополнительные функции, такие как экспорт данных, пагинацию и т.д.