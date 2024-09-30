import matplotlib.pyplot as plt

def plot_expenses(expense_data):  # Построение диаграммы расходов.
    categories = [row[0] for row in expense_data]
    amounts = [row[1] for row in expense_data]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='red')
    plt.title('Расходы по категориям')
    plt.xlabel('Категория расходов')
    plt.ylabel('Сумма расходов')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_incomes(income_data):  # Построение диаграммы доходов.
    categories = [row[0] for row in income_data]
    amounts = [row[1] for row in income_data]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='green')
    plt.title('Доходы по категориям')
    plt.xlabel('Категория доходов')
    plt.ylabel('Сумма доходов')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_income_vs_expenses(income_data, expense_data):  # Построение круговой диаграммы доходов и расходов.
    total_income = sum([row[1] for row in income_data])
    total_expense = sum([row[1] for row in expense_data])
    
    labels = ['Доходы', 'Расходы']
    amounts = [total_income, total_expense]

    plt.figure(figsize=(7, 7))
    plt.pie(amounts, labels=labels, autopct='%1.1f%%', colors=['green', 'red'])
    plt.title('Соотношение доходов и расходов')
    plt.show()


def get_expense_data(conn):  # Получение данных о расходах по категориям.
    with conn.cursor() as cur:
        cur.execute("""
            SELECT expense_categories.name, SUM(budget.expense_amount) 
            FROM budget
            JOIN expense_categories ON budget.expense_category_id = expense_categories.id
            WHERE budget.expense_amount IS NOT NULL
            GROUP BY expense_categories.name
        """)
        return cur.fetchall()

def get_income_data(conn):  # Получение данных о доходах по категориям.
    with conn.cursor() as cur:
        cur.execute("""
            SELECT income_categories.name, SUM(budget.income_amount) 
            FROM budget
            JOIN income_categories ON budget.income_category_id = income_categories.id
            WHERE budget.income_amount IS NOT NULL
            GROUP BY income_categories.name
        """)
        return cur.fetchall()
