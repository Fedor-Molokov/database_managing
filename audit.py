def initialize_audit_system(conn):
    audit_table_sql = """
    CREATE TABLE IF NOT EXISTS audit_log (
        id SERIAL PRIMARY KEY,
        table_name VARCHAR(255),
        operation_type VARCHAR(50),
        old_value TEXT,
        new_value TEXT,
        username VARCHAR(255),
        operation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    trigger_sql = """
    -- Функция триггера для INSERT
    CREATE OR REPLACE FUNCTION audit_insert()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO audit_log(table_name, operation_type, new_value, username)
        VALUES ('budget', 'INSERT', ROW(NEW.*), current_user);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Триггер для INSERT
    CREATE TRIGGER budget_insert AFTER INSERT ON budget
    FOR EACH ROW EXECUTE FUNCTION audit_insert();

    -- Функция триггера для UPDATE
    CREATE OR REPLACE FUNCTION audit_update()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO audit_log(table_name, operation_type, old_value, new_value, username)
        VALUES ('budget', 'UPDATE', ROW(OLD.*), ROW(NEW.*), current_user);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Триггер для UPDATE
    CREATE TRIGGER budget_update AFTER UPDATE ON budget
    FOR EACH ROW EXECUTE FUNCTION audit_update();

    -- Функция триггера для DELETE
    CREATE OR REPLACE FUNCTION audit_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO audit_log(table_name, operation_type, old_value, username)
        VALUES ('budget', 'DELETE', ROW(OLD.*), current_user);
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Триггер для DELETE
    CREATE TRIGGER budget_delete AFTER DELETE ON budget
    FOR EACH ROW EXECUTE FUNCTION audit_delete();

    """
    with conn.cursor() as cur:
        cur.execute(audit_table_sql)
        cur.execute(trigger_sql)
    print("Система аудита инициализирована.")

def view_audit_log(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM audit_log ORDER BY operation_timestamp DESC")
        records = cur.fetchall()
        for record in records:
            print(record)
