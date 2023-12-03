# IVI Test API Проект
## Обзор
**API IVI Test** - это веб-сервис, предназначенный для управления данными персонажей. Этот сервис позволяет пользователям создавать, читать, обновлять и удалять информацию о персонажах.

## Основные функции
**Управление персонажами**: операции CRUD для данных о персонажах.
**Версионированный API**: использует структуру версионированного API (/v2) для будущего масштабирования.
**Обработка ошибок**: всесторонняя обработка ошибок для различных крайних случаев и проверка ввода.

# Установка
## Требования
**Python 3.x**
Виртуальное окружение (рекомендуется)

## Настройка
Клонируйте репозиторий на локальный компьютер.
Перейдите в директорию проекта.
Настройте Python виртуальное окружение (опционально, но рекомендуется).
Установите необходимые зависимости:
'''pip install -r requirements.txt'''

# Использование

## Конечные точки API
Персонажи: Управление данными персонажей.

**GET** /v2/characters: Получение списка персонажей.
**GET** /v2/character: Получение конкретного персонажа.
**POST** /v2/character: Создание нового персонажа.
**PUT** /v2/character: Изменение персонажа.
**DELETE** /v2/character: Удаление персонажа.
**POST** /v2/reset: Сброс данных о персонажах.

# Тестирование
Запустите команду '''pytest --login=username --password=password''' для выполнения набора тестов.
Если нужно тестирование по маркерам, их можно просто добавить в строку pytest.
В проекте используется pytest для тестирования, включая функции, такие как повторный запуск неудачных тестов и параллельное выполнение.