# !/usr/bin/python
import psycopg2
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_tables():
    commands = (
        """ CREATE TABLE verdors 
        (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        );
        """,

        """ CREATE TABLE parts
        (
        part_id INTEGER PRIMARY KEY ,
        part_name VARCHAR(255) NOT NULL 
        );
        """,

        """
        CREATE TABLE part_drawings 
        (
        part_id INTEGER PRIMARY KEY ,
        file_extension VARCHAR(5) NOT NULL,
        drawing_data BYTEA NOT NULL,
        FOREIGN KEY (part_id)
        REFERENCES parts (part_id)
        ON UPDATE CASCADE ON DELETE CASCADE
        );
        """
    )

    conn = None

    try:
        connexionParams = config()
        conn = psycopg2.connect(**connexionParams)
        cur = conn.cursor()

        # create table by one
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_vendor(name):
    conn = None
    vendor_id = None

    sql = """INSERT INTO  vendors(vendor_name) VALUES (%s) RETURNING vendor_id; """
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, name)
        conn.commit()
        vendor_id = cur.fetchone()[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id


def insert_vendors(listNames):
    conn = None
    vendor_ids = None

    sql = """INSERT INTO  vendors(vendor_name) VALUES (%s); """
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, listNames)
        conn.commit()
        vendor_ids = cur.fetchone()[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return vendor_ids


if __name__ == '__main__':
    connect()
    # create_tables()
