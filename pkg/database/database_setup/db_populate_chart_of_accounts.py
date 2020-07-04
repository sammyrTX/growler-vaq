# db_populate_chart_of_accounts.py

"""load data for chart of accounts table"""

from db_test import create_connection, execute_query


# chart of accounts data
load_accounts = """
INSERT INTO chart_of_accounts (account_number, account_name, account_type)

VALUES
    (1010, "Cash - Regular Checking", 10),
    (1020, "Cash - Payroll Checking", 10),
    (1060, "Petty Cash Fund", 10),
    (1210, "Accounts Receivable", 10),
    (1250, "Allowance for Doubtful Accounts", 10),
    (1310, "Inventory", 10),
    (1410, "Supplies - Assets", 10),
    (1530, "Prepaid Insurance", 10),
    (1700, "Land", 10),
    (1710, "Buildings", 10),
    (1730, "Equipment", 10),
    (1780, "Vehicles", 10),
    (1810, "Accumulated Depreciation - Buildings", 10),
    (1830, "Accumulated Depreciation - Equipment", 10),
    (1880, "Accumulated Depreciation - Vehicles", 10),
    (2014, "Notes Payable - Credit Line #1", 20),
    (2024, "Notes Payable - Credit Line #2", 20),
    (2100, "Accounts Payable", 20),
    (2210, "Wages Payable", 20),
    (2310, "Interest Payable", 20),
    (2450, "Unearned Revenues", 20),
    (2510, "Mortgage Loan Payable", 20),
    (2560, "Bonds Payable", 20),
    (2565, "Discount on Bonds Payable", 20),
    (3710, "Common Stock, No Par", 30),
    (3750, "Retained Earnings", 30),
    (3950, "Treasury Stock", 30),
    (4101, "Sales - Division #1, Product Line 010", 40),
    (4102, "Sales - Division #1, Product Line 022", 40),
    (4201, "Sales - Division #2, Product Line 015", 40),
    (4411, "Sales - Division #4, Product Line 110", 40),
    (5101, "COGS - Division #1, Product Line 010", 50),
    (5102, "COGS - Division #1, Product Line 022", 50),
    (5201, "COGS - Division #2, Product Line 015", 50),
    (5311, "COGS - Division #3, Product Line 110", 50),
    (6010, "Salaries", 60),
    (6016, "Payroll Taxes", 60),
    (6020, "Supplies", 60),
    (6060, "Telephone", 60),
    (6070, "Computer", 60),
    (9180, "Gain on Sale of Assets", 70),
    (9610, "Loss on Sale of Assets", 70);
"""


if __name__ == '__main__':

    webdev_pw = '*** Need Password ***'
    connection = create_connection("localhost", "webdev", webdev_pw, "acctg_system")

    # select_accts = "SELECT * FROM accounts_old"
    # select_accts = "SELECT * FROM chart_of_accounts"
    execute_query(connection, load_accounts)

    print('*** End ***')
