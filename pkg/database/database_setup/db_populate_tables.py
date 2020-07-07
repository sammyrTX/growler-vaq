# db_populate_tables

"""
Populate the following tables for the acctg_system database

    chart_of_accounts
    currency
    departments
    entity
    periods


"""
import sys
import mysql.connector
from mysql.connector import Error

from db_populate_chart_of_accounts import load_accounts
from db_populate_currency import load_currency
from db_populate_departments import load_departments
from db_populate_entity import load_entity
from db_populate_periods import periods_list


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


if __name__ == '__main__':
    """Populate tables that will be part of the accounting web app
    database system.
    """

    webdev_pw = '*** Need password ***'

    try:
        connection = create_connection("localhost", "webdev", webdev_pw, "acctg_system")

    except mysql.Error as e:

        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Add error handling

    # Populate each table
    execute_query(connection, load_accounts)
    print('Chart of accounts loaded...')
    execute_query(connection, load_currency)
    print('Currency loaded...')
    execute_query(connection, load_departments)
    print('Departments loaded...')
    execute_query(connection, load_entity)
    print('Entities loaded...')

    # Populate periods table

    for _ in periods_list:
        load_period = """
        INSERT INTO periods (period, period_description, period_begin, period_end)

        VALUES (""" + str(_[0]) + """, '""" + _[1] + """', '""" + _[2] + """', '""" + _[3] + """');
        """
        execute_query(connection, load_period)
    print('Periods loaded...')

    print('*** End of tables load! ***')
