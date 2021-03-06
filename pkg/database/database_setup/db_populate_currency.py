# db_populate_currency.py

"""load data for currency table"""

from db_test import create_connection, execute_query

# currency data
load_currency = """
INSERT INTO currency (currency_code, currency_description)

VALUES
    ("USD", "US Dollars"),
    ("GBP", "British Pounds"),
    ("EUR", "Euros");
"""

if __name__ == '__main__':

    webdev_pw = '*** Need Password ***'
    connection = create_connection("localhost", "webdev", webdev_pw, "acctg_system")

    execute_query(connection, load_currency)

    print('*** End ***')
