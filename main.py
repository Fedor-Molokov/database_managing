import argparse
import psycopg2
import random
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from user_auth import create_user, authenticate_user
from audit import view_audit_log, initialize_audit_system
from view import view_income, view_expenses, view_budget_summary
from visualization import plot_expenses, get_income_data, plot_incomes, get_expense_data, plot_income_vs_expenses
from report import report_by_month, report_by_category, report_by_family_member


host = "localhost"
dbname = "my_database"
user = "my_user"
password = "my_password"

def create_connection():
    try:
        conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def initialize_data(conn):  # Добавление начальных данных в справочники.
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO relationship_types (name) VALUES ('Parent') RETURNING id")
            relationship_type_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO family_members (last_name, relationship_type_id) VALUES (%s, %s) RETURNING id",
                ('Ivanov', relationship_type_id)
            )
            family_member_id = cur.fetchone()[0]
            cur.execute("INSERT INTO expense_categories (name) VALUES ('Food') RETURNING id")
            expense_category_id = cur.fetchone()[0]
            cur.execute("INSERT INTO income_categories (name) VALUES ('Salary') RETURNING id")
            income_category_id = cur.fetchone()[0]
            return family_member_id, expense_category_id, income_category_id
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении начальных данных: {e}")
        return None, None, None

def add_expense(conn, date, family_member_id, expense_category_id, expense_amount):  # Добавление записи о расходе.
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO budget (date, family_member_id, expense_category_id, expense_amount) VALUES (%s, %s, %s, %s)",
                (date, family_member_id, expense_category_id, expense_amount)
            )
            print("Запись о расходе добавлена.")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении расхода: {e}")

def add_income(conn, date, family_member_id, income_category_id, income_amount):  # Добавление записи о доходе.
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO budget (date, family_member_id, income_category_id, income_amount) VALUES (%s, %s, %s, %s)",
                (date, family_member_id, income_category_id, income_amount)
            )
            print("Запись о доходе добавлена.")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении дохода: {e}")

def run_authentication_module(conn):  # Запуск модуля аутентификации пользователей.
    if input("Создать нового пользователя? (y/n): ") == 'y':
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        create_user(conn, username, password)
    username = input("Логин: ")
    password = input("Пароль: ")
    if authenticate_user(conn, username, password):
        print("Доступ разрешен.")
    else:
        print("Доступ запрещен.")

def get_random_data():  # Функция для генерации случайных данных о доходах или расходах.
    random_amount = round(random.uniform(100.00, 5000.00), 2)
    date = datetime.now().strftime('%Y-%m-%d')
    return date, random_amount

def interactive_add_income(conn):  # Интерактивный режим добавления записи о доходе.
    use_random = input("Вы хотите сгенерировать случайные данные? (y/n): ")
    if use_random.lower() == 'y':
        date, amount = get_random_data()
        print(f"Текущая дата: {date}")
        print(f"Случайная сумма дохода: {amount}")
    else:
        print("Введите данные для добавления дохода.")
        print("Пример формата даты: 2024-09-27")
        print("Пример суммы: 1500.50")
        while True:
            date = input("Введите дату дохода (формат: YYYY-MM-DD): ")
            try:
                datetime.strptime(date, '%Y-%m-%d')
                break
            except ValueError:
                print("Неверный формат даты, попробуйте снова.")
        while True:
            try:
                amount = float(input("Введите сумму дохода: "))
                break
            except ValueError:
                print("Неверный формат суммы, попробуйте снова.")
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM family_members LIMIT 1")
        family_member_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM income_categories LIMIT 1")
        income_category_id = cur.fetchone()[0]
    add_income(conn, date, family_member_id, income_category_id, amount)

def interactive_add_expense(conn):  # Интерактивный режим добавления записи о расходе.
    use_random = input("Вы хотите сгенерировать случайные данные? (y/n): ") # Спрашиваем у пользователя, хочет ли он сгенерировать случайные данные
    if use_random.lower() == 'y':
        date, amount = get_random_data()
        print(f"Текущая дата: {date}")
        print(f"Случайная сумма расхода: {amount}")
    else:
        print("Введите данные для добавления расхода.")
        print("Пример формата даты: 2024-09-27")
        print("Пример суммы: 500.50")
        while True:
            date = input("Введите дату расхода (формат: YYYY-MM-DD): ")
            try:
                # Проверяем формат даты
                datetime.strptime(date, '%Y-%m-%d')
                break
            except ValueError:
                print("Неверный формат даты, попробуйте снова.")
        while True:
            try:
                amount = float(input("Введите сумму расхода: "))
                break
            except ValueError:
                print("Неверный формат суммы, попробуйте снова.")
    with conn.cursor() as cur:      # Для примера выбираем первого члена семьи и категорию расходов
        cur.execute("SELECT id FROM family_members LIMIT 1")
        family_member_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM expense_categories LIMIT 1")
        expense_category_id = cur.fetchone()[0]

    add_expense(conn, date, family_member_id, expense_category_id, amount)

def main():
    parser = argparse.ArgumentParser(description='Управление функционалом приложения учета семейного бюджета.')
    parser.add_argument('--init-data', action='store_true', help='Запустить модуль инициализации данных.')
    parser.add_argument('--auth', action='store_true', help='Запустить модуль аутентификации пользователей.')
    parser.add_argument('--view-audit', action='store_true', help='Просмотреть журнал аудита изменений.')
    parser.add_argument('--add-expense', action='store_true', help='Добавить расход в бюджет интерактивно.')
    parser.add_argument('--add-income', action='store_true', help='Добавить доход в бюджет интерактивно.')
    parser.add_argument('--view-income', action='store_true', help='Просмотреть доходы.')
    parser.add_argument('--view-expenses', action='store_true', help='Просмотреть расходы.')
    parser.add_argument('--view-summary', action='store_true', help='Просмотреть сводный бюджет.')
    parser.add_argument('--plot-expenses', action='store_true', help='Построить график расходов.')
    parser.add_argument('--plot-incomes', action='store_true', help='Построить график доходов.')
    parser.add_argument('--plot-summary', action='store_true', help='Построить круговую диаграмму доходов и расходов.')
    parser.add_argument('--report-month', action='store_true', help='Отчет о доходах и расходах по месяцам.')
    parser.add_argument('--report-category', action='store_true', help='Отчет о доходах и расходах по категориям.')
    parser.add_argument('--report-family', action='store_true', help='Отчет о доходах и расходах по членам семьи.')
    args = parser.parse_args()

    conn = create_connection()
    if conn:
        print("Успешное подключение к базе данных.")
        if args.auth:
            run_authentication_module(conn)
        elif args.init_data:
            initialize_data(conn)
            print("Успешная инициализация данных.")
            initialize_audit_system(conn)
        elif args.view_audit:
            view_audit_log(conn)
        elif args.add_expense:
            interactive_add_expense(conn)
        elif args.add_income:
            interactive_add_income(conn)
        elif args.view_income:
            view_income(conn)
        elif args.view_expenses:
            view_expenses(conn)
        elif args.view_summary:
            view_budget_summary(conn)
        elif args.plot_expenses:
            expense_data = get_expense_data(conn)
            plot_expenses(expense_data)
        elif args.plot_incomes:
            income_data = get_income_data(conn)
            plot_incomes(income_data)
        elif args.plot_summary:
            income_data = get_income_data(conn)
            expense_data = get_expense_data(conn)
            plot_income_vs_expenses(income_data, expense_data)
        elif args.report_month:
            report_by_month(conn)
        elif args.report_category:
            report_by_category(conn)
        elif args.report_family:
            report_by_family_member(conn)
        else:
            parser.print_help()
            print("\nНе указана функция для запуска. Используйте один из доступных флагов.")
        conn.close()
    else:
        print("Не удалось подключиться к базе данных.")

if __name__ == "__main__":
    main()