import argparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from user_auth import create_user, authenticate_user
from audit import view_audit_log, initialize_audit_system

# Параметры подключения
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

def initialize_data(conn):
    """Добавление начальных данных в справочники."""
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

def add_expense(conn, date, family_member_id, expense_category_id, expense_amount):
    """Добавление записи о расходе."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO budget (date, family_member_id, expense_category_id, expense_amount) VALUES (%s, %s, %s, %s)",
                (date, family_member_id, expense_category_id, expense_amount)
            )
            print("Запись о расходе добавлена.")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении расхода: {e}")

def run_authentication_module(conn):
    """Запуск модуля аутентификации пользователей."""
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

def main():
    parser = argparse.ArgumentParser(description='Управление функционалом приложения учета семейного бюджета.')
    parser.add_argument('--init-data', action='store_true', help='Запустить модуль инициализации данных.')
    parser.add_argument('--auth', action='store_true', help='Запустить модуль аутентификации пользователей.')
    parser.add_argument('--view-audit', action='store_true', help='Просмотреть журнал аудита изменений.')
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
        else:
            parser.print_help()
            print("\nНе указана функция для запуска. Используйте один из доступных флагов.")
        conn.close()
    else:
        print("Не удалось подключиться к базе данных.")

if __name__ == "__main__":
    main()
