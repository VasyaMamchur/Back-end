from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2

def get_db_connection():
    return psycopg2.connect(host="dpg-clvk98la73kc73bqonrg-a", database="back_end_4gd4", user="back_end_4gd4_user", password="AsrTpmGMGkdBkoxPfEJ7rZmD7vLxtlRb")



def create_tables():
    commands = (
        """ 
        CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR (20) NOT NULL);
        """,
        """ 
        CREATE TABLE accounts (
                id SERIAL PRIMARY KEY,
                user_id INT,
                money INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
                );
        """,
        """ 
        CREATE TABLE categories ( 
                id SERIAL PRIMARY KEY, 
                name VARCHAR(20) NOT NULL 
                );
        """,
        """ 
        CREATE TABLE records ( 
                id SERIAL PRIMARY KEY,
                user_id INT,
                category_id INT, 
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                amount_of_expenditure FLOAT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
                );
        """)
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
create_tables()

import mymodule.views
import mymodule.models
