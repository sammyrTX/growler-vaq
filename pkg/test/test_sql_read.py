# test_sql_read.py

"""Test SQL read queries

    In order to run tests, run the following on the command line:
       <project_root_directory>$ python3 -m pytest -v
"""


import mysql.connector
from mysql.connector import Error
from .. database.db_config import config

from .. database.db_connection import (create_connection,
                                       execute_query,
                                       execute_read_query,
                                       )

from .. database.db_config import config

from .. database.sql_queries import queries_read

from .. database.sql_queries.queries_read import (select_all,
                                                  select_batch_available,
                                                  select_batch_loaded,
                                                  select_batch_by_row_id,
                                                  select_je_by_row_id,
                                                  select_rowcount_row_id,
                                                  select_batch_id,
                                                  batch_total,
                                                  select_entity_name_by_id,
                                                  select_entity_list,
                                                  get_gl_batch_status,
                                                  )

from .. database.sql_queries.queries_insert import (batch_load_je_file,
                                                    )

"""
Current READ queries:

x def select_all(table):
x def select_batch_available(table):
def select_batch_loaded(table):
def select_batch_by_row_id(table, journal_batch_row_id):
def select_je_by_row_id(table, row_id):
def select_rowcount_row_id(table, row_id):
def select_batch_id(table, journal_batch_row_id):
def batch_total(table, batch_row_id):
def select_entity_name_by_id(table, journal_batch_entity):
def select_entity_list():
def get_gl_batch_status(journal_batch_row_id):
"""

# Test functions to be used with pytest
value = 4000


def test_value():
    value_to_test = 4000

    assert(value == value_to_test)


def test_func_select_all():
    """Check row count from select_all function"""

    table = 'z_test_table_00'
    test_row_0 = (1, 'sample', 11.99)
    rows = select_all(table)
    rows_count = len(rows)
    test_value = 6

    assert(rows_count == test_value)
    assert(rows[0] == test_row_0)


def test_func_select_batch_available():
    """Check batches that should be available. gl_batch_status should
       not equal 20."""
    # table = 'z_test_journal_batch'
    # test_value = [(33, 'test-01', '888', 1, 0, 'NEED GL POST REF', 10), (32, 'test-00', 'lll', 1, 0, 'NEED GL POST REF', 10)]
    # rows = select_batch_available(table)

    # assert(rows == test_value)


# TODO
# Resume work here

def test_csv_load_process_not_ready():
    # Set up csv file to use
    filename = 'test01.csv'
    batch_row_id = 100

    # Load csv file to journal_loader
    load_file = batch_load_je_file(filename, batch_row_id)

    if load_file == 'LOAD OK':
        status = 1
    else:
        status = 99

    assert(status == 1)


# def test_func_select_batch_loaded_test_not_ready():
    """Check batches that have posted to the journal table."""

    # # test-csv_out01 Totals: DR/CR = 2,545,558.99
    # dr_cr_total = 2545558.99

    # # Need to determine which tables to use for this test
    # # Test tables or production tables in the development environment
    # table = 'z_test_journal_batch'
    # test_value = [(99, 'test-01', '888', 1, 0, 'NEED GL POST REF', 10), (32, 'test-00', 'lll', 1, 0, 'NEED GL POST REF', 10)]
    # # test_value = [(33, 'test-01', '888', 1, 0, 'NEED GL POST REF', 10), (32, 'test-00', 'lll', 1, 0, 'NEED GL POST REF', 10)]
    # rows = select_batch_available(table)

    # assert(dr_cr_total == 2545558.99)
    # assert(rows == test_value)


def test_query02():
    # test_value = (9, 'hotel-072820', 'hotel batch - test', 1, 1, 'NEED GL POST REF', 1)
    test_value = (33, 'take 5', '888', 1, 0, 'NEED GL POST REF', 10)

    table = 'journal_batch'
    journal_batch_row_id = 33
    row = select_batch_by_row_id(table, journal_batch_row_id)
    row = row[0]

    assert(row == test_value)


if __name__ == '__main__':

    """Test the select all rows query"""

    # table = 'chart_of_accounts'
    table = 'journal_batch'
    result_set = select_all(table)

    print('*' * 60)

    print(f'result_set:')

    for _ in result_set:
        print(_)
    print('*' * 60)

    print('')
    print('*' * 60)

    result_set = queries_read.select_batch_loaded('journal_batch')

    print(f'result_set:')
    print(f'{result_set}')
    print('')
    if result_set is None:
        print('Result set is empty')
    else:
        print(f'Result set is not empty')

    print('*' * 60)

    check_output = select_all('z_test_table_00')
    print('check_output:')
    print(f'{check_output}')
    print(f'items in check_output: {len(check_output)}')
    print('*' * 60)

    print('*' * 60)

    check_output = select_batch_available('z_test_journal_batch')
    print('check_output:')
    print(f'{check_output}')
    print(f'items in check_output: {len(check_output)}')
    print('*' * 60)

    print('*' * 60)

    check_output = select_batch_loaded('z_test_journal_batch')
    print('check_output:')
    print(f'{check_output}')
    print(f'items in check_output: {len(check_output)}')

    print('*' * 60)
