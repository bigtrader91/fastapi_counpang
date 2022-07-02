import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from psycopg2 import connect, extensions

engine = create_engine(
    f"postgresql://postgres:1234@localhost/coupang",
    echo=True,
)

conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password=1234,port=5432)

# SessionLocal = sessionmaker(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



def create_db(DB_NAME):

    cursor = conn.cursor()

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_isolation_level(autocommit)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE " + str(DB_NAME))
    print(f"{DB_NAME} Database created successfully...!")

    cursor.close
    conn.close()


def insert_data(df):
    df.to_sql(
        name='test',
        con=engine,
        if_exists="replace")

