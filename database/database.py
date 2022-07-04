from sqlalchemy import create_engine

import psycopg2
from psycopg2 import extensions

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


def insert_data(name,df,engine,if_exists='append' ):
    try:
        df.to_sql(
            name=name,
            con=engine,
            if_exists=if_exists)
    except Exception as ex:
        print("insert_data error :", ex)



items={
    '여성패션':1001,
    '남성패션':1002,
    '뷰티':1010,
    '출산/유아동':1011,
    '식품':1012,
    '주방용품':1013,
    '생활용품':1014,
    '홈인테리어':1015,
    '가전디지털':1016,
    '스포츠/레저':1017,
    '자동차용품':1018,
    '도서/음반/DVD':1019,
    '완구/취미':1020,
    '문구/오피스':1021,
    '헬스/건강식품':1024,
    '국내여행':1025,
    '해외여행':1026,
    '반려동물용품':1029,
    '유아동패션':1030
}


