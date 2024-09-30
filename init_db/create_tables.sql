CREATE TABLE IF NOT EXISTS relationship_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS family_members (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    relationship_type_id INTEGER REFERENCES relationship_types(id)
);

CREATE TABLE IF NOT EXISTS expense_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS income_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS budget (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    family_member_id INTEGER REFERENCES family_members(id),
    expense_category_id INTEGER REFERENCES expense_categories(id),
    expense_amount DECIMAL(10, 2),
    income_category_id INTEGER REFERENCES income_categories(id),
    income_amount DECIMAL(10, 2)
);

-- for python3 code modules

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(255),
    operation_type VARCHAR(50),
    old_value TEXT,
    new_value TEXT,
    username VARCHAR(255),
    operation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW income_view AS
SELECT 
    budget.id,
    family_members.last_name,
    income_categories.name AS income_category,
    budget.date,
    budget.income_amount
FROM 
    budget
JOIN 
    family_members ON budget.family_member_id = family_members.id
JOIN 
    income_categories ON budget.income_category_id = income_categories.id
WHERE 
    budget.income_amount IS NOT NULL;

CREATE VIEW expense_view AS
SELECT 
    budget.id,
    family_members.last_name,
    expense_categories.name AS expense_category,
    budget.date,
    budget.expense_amount
FROM 
    budget
JOIN 
    family_members ON budget.family_member_id = family_members.id
JOIN 
    expense_categories ON budget.expense_category_id = expense_categories.id
WHERE 
    budget.expense_amount IS NOT NULL;

CREATE VIEW budget_summary AS
SELECT 
    family_members.last_name,
    COALESCE(SUM(budget.income_amount), 0) AS total_income,
    COALESCE(SUM(budget.expense_amount), 0) AS total_expense,
    COALESCE(SUM(budget.income_amount), 0) - COALESCE(SUM(budget.expense_amount), 0) AS net_balance
FROM 
    budget
JOIN 
    family_members ON budget.family_member_id = family_members.id
GROUP BY 
    family_members.last_name;