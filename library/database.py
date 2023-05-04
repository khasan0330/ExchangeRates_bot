import psycopg2
import os
from dotenv import *
import time

load_dotenv()


def db_connect():
    database = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        host=os.getenv('DB_ADDRESS'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )

    return database


def create_table():
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aloqabank_history(
            history_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            date BIGINT,        
            currency_purchase VARCHAR(50),
            currency_sale VARCHAR(50),
            currency_cbu VARCHAR(50)
        );
        
        CREATE TABLE IF NOT EXISTS aloqabank_users(
            user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            telegram_id BIGINT UNIQUE   
        );
    ''')
    database.commit()
    database.close()


create_table()


def insert_or_ignore_user(user_id):
    database = db_connect()
    cursor = database.cursor()
    try:
        cursor.execute('''
        INSERT INTO aloqabank_users(telegram_id) VALUES (%s)
        ''', (user_id,))
        database.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        return False
    finally:
        database.close()


def insert_currency(purchase, sale, cbu):
    unix_time = int(time.time())
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO aloqabank_history(date, currency_purchase, currency_sale, currency_cbu)
    VALUES (%s, %s, %s, %s)
    ''', (unix_time, purchase, sale, cbu))
    database.commit()
    database.close()


def get_last_currency():
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT currency_purchase, currency_sale, currency_cbu 
    FROM aloqabank_history 
    ORDER BY history_id DESC LIMIT 1;
    ''')
    result = cursor.fetchone()
    database.close()
    return result


def get_all_users():
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT telegram_id FROM aloqabank_users;
    ''')
    users = cursor.fetchall()
    database.close()
    return users


def del_block(user_id):
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM aloqabank_users WHERE telegram_id = %s;
    ''', (user_id,))
    database.commit()
    database.close()



