'''
source: [Python and MySQL Database: A Practical Introduction – Real Python](https://realpython.com/python-mysql/#installing-mysql-server-and-mysql-connectorpython)
'''

import mysql.connector

import pprint

from getpass import getpass
from mysql.connector import connect, Error

## Create a database

def create_menzies_stock_database(connection):
    try:
        create_db_query = "CREATE DATABASE menzies_wine_stock"
        
        with connection.cursor() as cursor:
            
            cursor.execute(create_db_query)

            show_db_query = 'SHOW DATABASES'
            
            with connection.cursor() as cursor:
                cursor.execute(show_db_query)
                for db in cursor:
                    print(db)

    except Error as e:
        print(e)

def create_menzies_stock_table(connection):

    try:
        with connection.cursor() as cursor:
            
            create_menzies_stock_table_query = """
            CREATE TABLE menzies_wine_stock(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            vintage YEAR(4),
            soh FLOAT(3,2),
            par SMALLINT(3),
            restock FLOAT(3,2),
            report_low VARCHAR(100),
            other_locations VARCHAR(100),
            vial SMALLINT(4)
            )
            """
        
            cursor.execute(create_menzies_stock_table_query)
            connection.commit()

    except Error as e:
        print(e)

def view_table_schema(connection):
    """ 
    View a table schema
    """
    try:
        with connection.cursor() as cursor:
            show_table_query = """
            DESCRIBE menzies_wine_stock
            """
            cursor.execute(show_table_query)
            result = cursor.fetchall()
            for row in result:
                print(row)
    except:
        print('error')

def alter_menzies_table(connection):
    try:
        with connection.cursor() as cursor:
            show_table_query = """
            ALTER TABLE menzies_wine_stock report_low TO dont_report
            """

            cursor.execute(show_table_query)
    except:
        print("error")

def main():
    connection_ = connect(
        host="localhost",
        user="root",
        password="S74rg4z3r",
        database="menzies_wine_stock",
        )

    # create_menzies_stock_database()

    # create_menzies_stock_table()   

    # view_table_schema(connection_)
    
    #alter_menzies_table(connection)

    try:
        
        with connection_ as cnx:
            cursor = cnx.cursor()
            cursor.execute("SHOW TABLES")
            result = cursor.fetchall()
            
            add_columns_query="""
            ALTER TABLE menzies_wine_stock
                ADD format VARCHAR(100) NOT NULL
                    AFTER name,
                ADD category VARCHAR(100) NOT NULL
                    AFTER format;
            """

            #cursor.execute(add_columns_query)
            #result = cursor.fetchall()

            cursor.execute("SHOW COLUMNS FROM menzies_wine_stock")
            result = cursor.fetchall()
            
            #print(result)
            
            pp = pprint.PrettyPrinter(indent=4)

            pp.pprint(result)

    except Error as e:
        print(e)

main()

