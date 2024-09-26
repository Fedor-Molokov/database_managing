-- Таблица для учета бюджета
CREATE TABLE budget (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    family_member_id INTEGER REFERENCES family_members(id),
    expense_category_id INTEGER REFERENCES expense_categories(id),
    expense_amount DECIMAL(10, 2),
    income_category_id INTEGER REFERENCES income_categories(id),
    income_amount DECIMAL(10, 2)
);

-- Справочник членов семьи
CREATE TABLE family_members (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    relationship_type_id INTEGER REFERENCES relationship_types(id)
);

-- Справочник статей расходов
CREATE TABLE expense_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Справочник статей доходов
CREATE TABLE income_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Справочник видов родства
CREATE TABLE relationship_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
