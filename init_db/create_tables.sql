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
