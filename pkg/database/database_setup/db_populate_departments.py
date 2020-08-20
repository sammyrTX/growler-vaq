# db_populate_departments.py

"""load data for departments table"""

from db_test import create_connection, execute_query

# departments data
load_departments = """
INSERT INTO departments (department_number, department_name)

VALUES
    (250, "Sales - APAC - Australia"),
    (200, "Sales - North America"),
    (300, "Engineering - TX - Austin"),
    (500, "Operations - NA"),
    (100, "Accounting - Corporate HQ");
"""

if __name__ == '__main__':

    webdev_pw = '*** Need Password ***'
    connection = create_connection("localhost", "webdev", webdev_pw, "acctg_system")

    execute_query(connection, load_departments)

    print('*** End ***')
