-- Виды родства
INSERT INTO relationship_types (name) VALUES
('Отец'), 
('Мать'), 
('Сын'), 
('Дочь');

-- Статьи расходов
INSERT INTO expense_categories (name) VALUES
('Продукты питания'),
('Оплата жилья'),
('Коммунальные услуги'),
('Транспорт'),
('Развлечения');

-- Статьи доходов
INSERT INTO income_categories (name) VALUES
('Зарплата'),
('Пенсия'),
('Стипендия'),
('Доход от бизнеса');
