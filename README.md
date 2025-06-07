![Tests](https://github.com/ivanov-dv/ff2_telegram_ui/actions/workflows/main.yml/badge.svg)

# Family finance telegram user interface

Микросервис для взаимодействия через Telegram интерфейс с пользователями сервиса Family Finance.
***

## Применяемые библиотеки и технологии:
- Python 3.12;
- Aiogram;
- Async-lru;
- Pytest;
- Poetry;
- Docker;
- Kubernetes;
- CI/CD.

## Установка и запуск
#### Для работы необходим запущенный [API сервис](https://github.com/ivanov-dv/family_finances_2).
1. Клонируйте репозиторий.
2. Укажите необходимые переменные в файле `.env`.
3. Запустите приложение с помощью Docker Compose. 
Из корневой папки репозитория выполните команду `docker compose up -d`

Сервис доступен в телеграм боте, ключ которого вы укажете в файле`.env`.
