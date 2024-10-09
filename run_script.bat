@echo off

REM Установка пакетов с помощью pip
pip install psycopg2-binary
pip install bcrypt
pip install matplotlib

REM Запуск Docker Compose
docker-compose up -d

REM Пауза на 30 секунд
sleep 30

REM Подключение к PostgreSQL через psql
psql -h localhost -p 5432 -U my_user -d my_database