#!/bin/bash

pip3 install psycopg2-binary
pip3 install bcrypt
pip3 install matplotlib

docker compose up -d
sleep 2
psql -h localhost -p 5432 -U my_user -d my_database
