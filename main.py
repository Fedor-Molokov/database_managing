import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Параметры подключения
host = "localhost"
dbname = "my_database"
user = "my_user"
password = "my_password"

# Функция для создания соединения
def create_connection():
    try:
        conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

# Функция для добавления начальных данных
def initialize_data(conn):
    """Добавление начальных данных в справочники."""
    try:
        with conn.cursor() as cur:
            # Добавление типов родства
            cur.execute("INSERT INTO relationship_types (name) VALUES ('Parent') RETURNING id")
            relationship_type_id = cur.fetchone()[0]

            # Добавление членов семьи
            cur.execute(
                "INSERT INTO family_members (last_name, relationship_type_id) VALUES (%s, %s) RETURNING id",
                ('Ivanov', relationship_type_id)
            )
            family_member_id = cur.fetchone()[0]

            # Добавление категорий расходов
            cur.execute("INSERT INTO expense_categories (name) VALUES ('Food') RETURNING id")
            expense_category_id = cur.fetchone()[0]

            # Добавление категорий доходов
            cur.execute("INSERT INTO income_categories (name) VALUES ('Salary') RETURNING id")
            income_category_id = cur.fetchone()[0]

            return family_member_id, expense_category_id, income_category_id
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении начальных данных: {e}")
        return None, None, None

# Функция для добавления записи о расходе
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

# Главная функция
def main():
    conn = create_connection()
    if conn:
        print("Успешное подключение к базе данных.")
        family_member_id, expense_category_id, income_category_id = initialize_data(conn)
        if family_member_id and expense_category_id and income_category_id:
            add_expense(conn, '2024-09-27', family_member_id, expense_category_id, 500.00)
        conn.close()
    else:
        print("Не удалось подключиться к базе данных.")

if __name__ == "__main__":
    main()
