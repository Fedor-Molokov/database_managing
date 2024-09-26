#!/bin/bash


# pip3 install psycopg2-binary

docker compose up -d
sleep 2
psql -h localhost -p 5432 -U my_user -d my_database
