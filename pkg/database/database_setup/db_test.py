import mysql.connector
from mysql.connector import Error


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


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

webdev_pw = '<replace with password>'


if __name__ == '__main__':
    connection = create_connection("localhost", "webdev", webdev_pw, "acctg_system")

    # select_accts = "SELECT * FROM accounts_old"
    select_accts = "SELECT * FROM chart_of_accounts"
    accts_ = execute_read_query(connection, select_accts)

    for _ in accts_:
        print(_)
