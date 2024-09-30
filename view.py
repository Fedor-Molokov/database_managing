def view_income(conn):
    """Отображение доходов с использованием представления income_view."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM income_view")
            rows = cur.fetchall()
            print("\nДоходы:")
            for row in rows:
                print(f"ID: {row[0]}, Фамилия: {row[1]}, Категория дохода: {row[2]}, Дата: {row[3]}, Сумма: {row[4]}")
    except psycopg2.Error as e:
        print(f"Ошибка при выполнении запроса к представлению income_view: {e}")

def view_expenses(conn):
    """Отображение расходов с использованием представления expense_view."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM expense_view")
            rows = cur.fetchall()
            print("\nРасходы:")
            for row in rows:
                print(f"ID: {row[0]}, Фамилия: {row[1]}, Категория расхода: {row[2]}, Дата: {row[3]}, Сумма: {row[4]}")
    except psycopg2.Error as e:
        print(f"Ошибка при выполнении запроса к представлению expense_view: {e}")

def view_budget_summary(conn):
    """Отображение сводного бюджета с использованием представления budget_summary."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM budget_summary")
            rows = cur.fetchall()
            print("\nСводный бюджет:")
            for row in rows:
                print(f"Фамилия: {row[0]}, Общий доход: {row[1]}, Общие расходы: {row[2]}, Баланс: {row[3]}")
    except psycopg2.Error as e:
        print(f"Ошибка при выполнении запроса к представлению budget_summary: {e}")
