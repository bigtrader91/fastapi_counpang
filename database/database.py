import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from psycopg2 import connect, extensions

engine = create_engine(
    f"postgresql://postgres:postgres@localhost/coupang",
    echo=True,
)

conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password='postgres',port=5432)

def create_db(DB_NAME):

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_isolation_level(autocommit)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE " + str(DB_NAME))
    print(f"{DB_NAME} Database created successfully...!")

    cursor.close
    conn.close()


def insert_data(name,df,if_exists='append'):
    try:
        df.to_sql(
            name=name,
            con=engine,
            if_exists=if_exists)
    except Exception as ex:
        print("insert_data error :", ex)



# SessionLocal = sessionmaker(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




