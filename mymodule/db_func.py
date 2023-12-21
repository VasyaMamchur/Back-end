import psycopg2
from mymodule import db
def get_db_connection():
    return psycopg2.connect(host="dpg-cm041ned3nmc738j45bg-a", database="back_end_1vxx", user="admin", password="zROLWMZmaXBWInlu4wHHV4sh11MgH3kF")


def add(data):
    db.session.add(data)
    db.session.commit()


def update():
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()

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