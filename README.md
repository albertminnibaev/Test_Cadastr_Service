# Тестовое задание для Backend разработчика (junior)
1. Перед началом работы в корне проекта необходимо создать файл .env для хранения переменных окружения.
Файл .env создается на основе файла .env.sample.
Файл .env содержит следующие переменные:
   * SECRET_KEY - секретный ключ Django;
   * PASSWORD_DATABASE - пароль для подключения к базе данных;
   * POSTGRES_DB - имя при подключении к базе данных при помощи Docker-Compose (postgres);
   * POSTGRES_USER - имя при подключении к базе данных при помощи Docker-Compose (postgres);
   * POSTGRES_PASSWORD - пароль при подключении к базе данных при помощи Docker-Compose;
   * PGDATA - при подключении к базе данных при помощи Docker-Compos (/var/lib/postgresql/data/pgdata);

2. Для регистрации и аутентификации используется стандартные инструменты Django REST framework с использованием библиотеку djangorestframework-simplejwt
3. Для запуска проекта необходимо запустить само приложение коммандой - python manage.py runserver
4. Для запуска проекта при помощи Docker-Compose необходимо в файле settings.py активировать соответствующие настройки
5. Написаны тесты функционала.
   Для запуска тестов и получения отчёта использовать следующие команды
   - docker-compose exec app coverage run --source='.' manage.py test
   - docker-compose exec app coverage report

## Описание документации к API:
Для автоматического генерирования документации используются Swagger и Redoc.
Пример основных запросов:
1. Получения запроса:


    запрос POST /query
    необходимо передать в параметрах кадастровый номер (cadastral_number) в формате АА:ВВ:CCCCСCC:КК, 
    широту (latitude) в диапазоне от -90 до 90 и долготу (longitude) в диапазоне от -180 до 180
    {
      "cadastral_number": "string",
      "latitude": "string",
      "longitude": "string"
    }

    ответ: 

    статус код: 200 OK

    {
      "message": "Запрос зарегистрирован. Номер вашего обращения 1"
    }

2. Получение результата запроса:


    запрос POST /result
    Необходимо передать в параметрах номер запроса (number_request)
    {
      "number_request": "string"
    }

    ответ: 

    статус код: 200 OK

    {
      "message": "Статус запроса: Успешно"
    }

3. Получение информации о том, что сервер запущен:


    запрос GET /ping

    ответ: 

    статус код: 200 OK

    {
      "message": "Сервер запущен"
    }

4. получение истории запросов, принадлежащих только одному кадастровому номеру:


    запрос POST /history_number
    Необходимо передать в параметрах кадастровый номер (cadastral_number) в формате АА:ВВ:CCCCСCC:КК,
    {
      "cadastral_number": "string"
    }

    ответ: 

    статус код: 200 OK

    {
      "message": [
        {
          "id": "string",
          "cadastral_number": "string",
          "latitude": "string",
          "longitude": "string",
          "created_at": "string"",
          "server_response": "string"
        }]
    }

5. получение истории всех запросов:


    запрос POST /history

    ответ: 

    статус код: 200 OK

    {
     "count": 1,
     "next": null,
     "previous": null,
     "results": [
        {
          "id": "string",
          "cadastral_number": "string",
          "latitude": "string",
          "longitude": "string",
          "created_at": "string"",
          "server_response": "string"
        }]
     }
