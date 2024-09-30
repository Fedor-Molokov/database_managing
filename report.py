import psycopg2
from datetime import datetime

def report_by_month(conn):  # Отчет о доходах и расходах по месяцам
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    TO_CHAR(budget.date, 'YYYY-MM') AS month,
                    COALESCE(SUM(budget.income_amount), 0) AS total_income,
                    COALESCE(SUM(budget.expense_amount), 0) AS total_expense
                FROM budget
                GROUP BY TO_CHAR(budget.date, 'YYYY-MM')
                ORDER BY month;
            """)
            rows = cur.fetchall()
            print("\nОтчет о доходах и расходах по месяцам:")
            for row in rows:
                print(f"Месяц: {row[0]}, Доходы: {row[1]}, Расходы: {row[2]}")
    except psycopg2.Error as e:
        print(f"Ошибка при создании отчета по месяцам: {e}")

def report_by_category(conn):  # Отчет о доходах и расходах по категориям.
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    'Доходы' AS type,
                    income_categories.name AS category,
                    SUM(budget.income_amount) AS total_amount
                FROM budget
                JOIN income_categories ON budget.income_category_id = income_categories.id
                WHERE budget.income_amount IS NOT NULL
                GROUP BY income_categories.name
                UNION ALL
                SELECT
                    'Расходы' AS type,
                    expense_categories.name AS category,
                    SUM(budget.expense_amount) AS total_amount
                FROM budget
                JOIN expense_categories ON budget.expense_category_id = expense_categories.id
                WHERE budget.expense_amount IS NOT NULL
                GROUP BY expense_categories.name;
            """)
            rows = cur.fetchall()
            print("\nОтчет о доходах и расходах по категориям:")
            for row in rows:
                print(f"Тип: {row[0]}, Категория: {row[1]}, Сумма: {row[2]}")
    except psycopg2.Error as e:
        print(f"Ошибка при создании отчета по категориям: {e}")

def report_by_family_member(conn):  # Отчет о доходах и расходах по членам семьи.
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    family_members.last_name AS family_member,
                    COALESCE(SUM(budget.income_amount), 0) AS total_income,
                    COALESCE(SUM(budget.expense_amount), 0) AS total_expense
                FROM budget
                JOIN family_members ON budget.family_member_id = family_members.id
                GROUP BY family_members.last_name
                ORDER BY family_members.last_name;
            """)
            rows = cur.fetchall()
            print("\nОтчет о доходах и расходах по членам семьи:")
            for row in rows:
                print(f"Член семьи: {row[0]}, Доходы: {row[1]}, Расходы: {row[2]}")
    except psycopg2.Error as e:
        print(f"Ошибка при создании отчета по членам семьи: {e}")
