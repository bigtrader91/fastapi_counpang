
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from psycopg2 import connect, extensions

conn = psycopg2.connect(host='localhost', database='postgres',user='postgres',password='postgres',port=5432)
def create_db(DB_NAME):

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_isolation_level(autocommit)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE " + str(DB_NAME))
    print(f"{DB_NAME} Database created successfully...!")

    cursor.close
    conn.close()

create_db('coupang')