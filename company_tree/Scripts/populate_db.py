import sys
import os
import django
import random
from faker import Faker
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Абсолютный путь до каталога с manage.py
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# Установка переменной окружения для настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_tree.settings")

# Инициализация Django
django.setup()

from employees.models import Department, Employee
from django.core.management import call_command

fake = Faker()

def reset_database():
    # Удаляем старую базу данных и создаем новую
    db_path = os.path.join(base_dir, 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)
        logging.info("Старая база данных удалена.")
    else:
        logging.info("Файл базы данных не найден, создание новой базы данных.")

    # Выполняем миграции для создания новой базы данных
    call_command('migrate', verbosity=0)
    logging.info("Миграции выполнены.")

def create_departments_recursive(parent, level, max_level, departments_per_level):
    departments = []
    if level > max_level:
        return departments
    for _ in range(departments_per_level.get(level, 1)):
        dept = Department.objects.create(
            name=fake.company(),
            parent=parent
        )
        departments.append(dept)
        logging.debug(f"Создан отдел '{dept.name}' на уровне {level}")
        departments.extend(create_departments_recursive(dept, level + 1, max_level, departments_per_level))
    return departments

def create_departments():
    departments_per_level = {
        1: 5,
        2: 4,
        3: 2,
        4: 1,
        5: 1
    }
    max_level = 5
    logging.info("Создание отделов...")

    company = Department.objects.create(name=fake.company())
    logging.info(f"Создана главная компания '{company.name}'")

    all_departments = [company]
    all_departments.extend(create_departments_recursive(company, 1, max_level, departments_per_level))

    logging.info(f"Всего создано отделов: {len(all_departments)}")
    return all_departments

def create_employees(n, departments):
    logging.info("Создание сотрудников...")

    # Получаем самые нижние отделы (без подотделов)
    deepest_departments = [dept for dept in departments if not dept.get_children().exists()]
    logging.info(f"Количество нижних отделов: {len(deepest_departments)}")

    employees = []
    for i in range(n):
        dept = random.choice(deepest_departments)
        emp = Employee(
            full_name=fake.name(),
            position=fake.job(),
            hire_date=fake.date_between(start_date="-10y", end_date="today"),
            salary=round(random.uniform(30000.0, 200000.0), 2),
            department=dept
        )
        employees.append(emp)

        if (i + 1) % 5000 == 0:
            Employee.objects.bulk_create(employees)
            logging.info(f"Создано сотрудников: {i + 1}")
            employees = []

    if employees:
        Employee.objects.bulk_create(employees)
        logging.info(f"Создано сотрудников: {n}")

if __name__ == '__main__':
    reset_database()
    departments = create_departments()
    employee_count = 50000
    create_employees(employee_count, departments)
    logging.info("Генерация данных завершена!")
