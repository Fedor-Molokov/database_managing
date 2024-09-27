import bcrypt

def create_user(conn, username, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash.decode('utf-8'))  # Обеспечивает сохранение в виде строки
            )
            print("Пользователь создан.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании пользователя: {e}")

def authenticate_user(conn, username, password):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT password_hash FROM users WHERE username = %s",
            (username,)
        )
        result = cur.fetchone()
        if result:
            password_hash = result[0]
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                print("Аутентификация успешна.")
                return True
            else:
                print("Неверные логин или пароль.")
        else:
            print("Пользователь не найден.")
        return False

