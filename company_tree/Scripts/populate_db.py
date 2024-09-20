import sys
import os
import django
import random
from faker import Faker

# Абсолютный путь до каталога на уровне manage.py
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# Установка переменной окружения для настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_tree.settings")

# Инициализация Django
django.setup()

from employees.models import Department, Employee
from django.core.management import call_command

fake = Faker()

def create_departments():
    # Удаляем старую базу данных и создаем новую
    db_path = os.path.join(base_dir, 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Старая база данных удалена.")

    # Выполняем миграции для создания новой базы данных
    call_command('migrate')

    # Создаем главную компанию
    company = Department.objects.create(name=fake.company())
    all_departments = [company]

    # Уровень 1 (подразделения главной компании)
    level1_departments = []
    for _ in range(5):
        dept = Department.objects.create(
            name=fake.company(),
            parent=company
        )
        level1_departments.append(dept)
        all_departments.append(dept)

    # Уровень 2 (подразделения подразделений)
    level2_departments = []
    for parent_dept in level1_departments:
        for _ in range(4):  # Создаем 4 подразделения для каждого отдела уровня 1
            dept = Department.objects.create(
                name=fake.company(),
                parent=parent_dept
            )
            level2_departments.append(dept)
            all_departments.append(dept)

    # Уровень 3 (подразделения уровня 2)
    level3_departments = []
    for parent_dept in level2_departments:
        for _ in range(2):  # Создаем 2 подразделения для каждого отдела уровня 2
            dept = Department.objects.create(
                name=fake.company(),
                parent=parent_dept
            )
            level3_departments.append(dept)
            all_departments.append(dept)

    # Уровень 4 (подразделения уровня 3)
    level4_departments = []
    for parent_dept in level3_departments:
        dept = Department.objects.create(
            name=fake.company(),
            parent=parent_dept
        )
        level4_departments.append(dept)
        all_departments.append(dept)

    # Уровень 5 (подразделения уровня 4)
    level5_departments = []
    for parent_dept in level4_departments:
        dept = Department.objects.create(
            name=fake.company(),
            parent=parent_dept
        )
        level5_departments.append(dept)
        all_departments.append(dept)

    return all_departments

def create_employees(n, departments):
    # Распределяем сотрудников по самым нижним подразделениям (уровень 5)
    deepest_departments = [dept for dept in departments if dept.get_children().count() == 0]
    for _ in range(n):
        dept = random.choice(deepest_departments)
        Employee.objects.create(
            full_name=fake.name(),
            position=fake.job(),
            hire_date=fake.date_between(start_date="-10y", end_date="today"),
            salary=round(random.uniform(30000.0, 200000.0), 2),
            department=dept
        )

if __name__ == '__main__':
    # Создаем отделы и сотрудников
    departments = create_departments()

    # Общее количество сотрудников
    employee_count = 50000

    create_employees(employee_count, departments)

    print("Data generation complete!")
