# Сервисный центр SaintSir

## Camunda Technical Support System

- Управление задачами и уведомлениями.
- Использует Camunda BPM для управления процессами.
- Интеграция с Keycloak для управления пользователями и ролями.
```sh
    docker compose -f /mnt/work/Programs/camunda/camunda-distributions/docker-compose/versions/camunda-8.7/docker-compose.yaml up -d
``` 

## Backend 

- Python 3.11 для разработки серверной части.
- FastAPI для создания RESTful API.
- SQLAlchemy для работы с базой данных.
- PostgreSQL в качестве базы данных.

### Приложения
- bpmn - Управление процессами и задачами в Camunda.
- reference - Управление лидами и из задачами.

## Frontend

- Nuxt.js для создания пользовательского интерфейса.
- Axios для работы с API.

## Установка и запуск

```bash
# backend
cd backend
source venv/bin/activate
python main.py
```

```bash
# frontend
cd frontend
npm run dev
```

## Авторизация, аутентификация и безопасность
- Используется Keycloak для управления пользователями и ролями.
- FastAPI Keycloak Middleware для интеграции с Keycloak.

### Настройки Keycloak
- Зайти в Keycloak Admin Console. http://localhost:18080/auth/admin/master/console/#/camunda-platform
- Перейти в реальм `camunda-platform`.
- Создать клиента `fastapi-client` с доступом к API.
- Указать данные в `.env` файле:
```env
KEYCLOAK_AUTH_SERVER_URL=http://localhost:18080/auth/
KEYCLOAK_REALM=camunda-platform
KEYCLOAK_CLIENT_ID=fastapi-client
KEYCLOAK_CLIENT_SECRET=your-client-secret
```

