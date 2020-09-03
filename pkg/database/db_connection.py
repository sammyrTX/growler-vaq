# db_connection.py
"""functions to create a connection to a mysql database"""

import mysql.connector
from mysql.connector import Error
from . db_config import config


def create_connection(user, password, host, database):
    """Connection to a MySQL database"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        print("Connection to MySQL DB successful")
    except ConnectionError as e:
        print(f"The connection error '{e}' occurred")
    except mysql.connector.Error as err:
        print(f'Something went wrong: {err}')
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    """Execute a SQL query passed as an argument"""

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return "Query executed successfully"
    except Error as e:
        return f'The error "{e}" occurred'
    # Original code
    # try:
    #     cursor.execute(query)
    #     connection.commit()
    #     print("Query executed successfully")
    # except Error as e:
    #     print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    """Execute a select query"""
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


if __name__ == '__main__':
    connection = create_connection(**config)

    select_accts = "SELECT * FROM chart_of_accounts"
    print(f'query string: {select_accts}')

    accts_ = execute_read_query(connection, select_accts)

    for _ in accts_:
        print(_)
