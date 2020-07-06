# db_populate_entity.py

"""load data for currency table"""

from db_test import create_connection, execute_query

# currency data
load_entity = """
INSERT INTO entity (entity_name, entity_currency)

VALUES
    ("North America", "USD"),
    ("UK - London", "GBP"),
    ("Germany - Frankfurt", "EUR");
"""

if __name__ == '__main__':

    webdev_pw = '*** Need Password ***'
    connection = create_connection("localhost", "webdev", webdev_pw, "acctg_system")

    execute_query(connection, load_entity)

    print('*** End ***')
