import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Параметры подключения
host = "localhost"
dbname = "my_database"
user = "my_user"
password = "my_password"

# Функция для создания соединения
def create_connection():
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

# Функция для добавления записи о расходе
def add_expense(conn, date, family_member_id, expense_category_id, expense_amount):
    """Добавление записи о расходе."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO budget (date, family_member_id, expense_category_id, expense_amount)
                VALUES (%s, %s, %s, %s)
                """,
                (date, family_member_id, expense_category_id, expense_amount)
            )
            print("Запись о расходе добавлена.")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении расхода: {e}")

# Главная функция
def main():
    # Создание подключения
    conn = create_connection()
    if conn:
        print("Успешное подключение к базе данных.")
        
        # Тестовые данные для добавления расхода
        add_expense(conn, '2024-09-27', 1, 1, 500.00)
        
        # Закрытие соединения
        conn.close()
    else:
        print("Не удалось подключиться к базе данных.")

if __name__ == "__main__":
    main()
