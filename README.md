# Company Tree Application

Это Django-приложение для отображения древовидной структуры компании с отделами и сотрудниками. Оно использует библиотеку `django-mptt` для работы с иерархическими данными и Bootstrap для стилизации интерфейса.

## Функциональность

- Отображение дерева отделов и сотрудников.
- Скрипт для заполнения базы данных тестовыми данными.
- Интерактивный интерфейс с возможностью сворачивания и разворачивания разделов.
- Кастомная стилизация с использованием Twitter Bootstrap и Font Awesome.

## Требования

- Python 3.6 или выше
- Django 3.2 или выше
- Библиотека `django-mptt`
- Библиотека `Faker`
- Bootstrap 4.5
- Font Awesome

## Инструкции по установке

### 1. Клонирование репозитория

```bash
git clone https://github.com/Runya1337/TL_test
cd test_TL
```

### 2. Создание и активация виртуального окружения
Рекомендуется использовать виртуальное окружение для управления зависимостями.
#### На macOS и Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```
#### На Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Установка Зависимостей 
```bash
pip install -r requirements.txt
```
### 3.1 Переход в Django-проект 
```bash
cd company_tree
```

### 4. Создание и применение миграций и сбор статики
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```
### 5. Заполнение базы данных
Запустите скрипт для генерации тестовых данных
```bash
python Scripts/populate_db.py
```
### 6. Запуск сервера разработки
```bash
python manage.py runserver
```
### 6. Запуск сервера разработки
http://127.0.0.1:8000/employees/tree/




