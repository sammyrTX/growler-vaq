# test_sql_read.py

"""Test SQL read queries

    In order to run tests, run the following on the command line:
       <project_root_directory>$ python3 -m pytest -v
"""


import mysql.connector
from mysql.connector import Error
from .. database.db_config import config, working_data_folder
from .. database.db_connection import (create_connection,
                                       execute_query,
                                       execute_read_query,
                                       )

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
                                                  get_journal_batch_row_id_by_name,
                                                  )

from .. database.sql_queries.queries_insert import (batch_load_je_file,
                                                    insert_new_batch_name,
                                                    batch_load_insert,
                                                    )

from . test_queries import query_initialize_000

import pandas as pd

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

# Values to be used within scope of test_sql_read.py
test_filename = 'csv_out00.csv'
test_journal_batch_name = 'pytest-test_csv_load9'
test_journal_batch_description = 'csv_out00.csv'
test_journal_batch_entity = 1
test_journal_batch_currency = 1
test_gl_post_reference = 'NULL'
test_gl_batch_status = 0

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


def test_func_select_batch_available_not_ready():
    pass
    """Check batches that should be available. gl_batch_status should
       not equal 20."""
    # table = 'z_test_journal_batch'
    # test_value = [(33, 'test-01', '888', 1, 0, 'NEED GL POST REF', 10), (32, 'test-00', 'lll', 1, 0, 'NEED GL POST REF', 10)]
    # rows = select_batch_available(table)

    # assert(rows == test_value)


def test_csv_load_process():
    """Create a batch and then load a csv file into journal_loader and then
    into journal. Check if it loads into journal_loader. If that passes check
    if it loads into journal by comparing DR/CR totals from the journal table
    versus the same csv file loaded into a pandas dataframe.
    """

    # Initialize journal_batch, journal_loader and journal by deleting all
    # rows from each table

    table_list = ['journal_batch',
                  'journal_loader',
                  # 'journal_loaderX',
                  'journal',
                  ]

    initialize_result = query_initialize_000(table_list)

    if initialize_result[0] != 0:
        print(initialize_result[1])
        raise Exception('Table initialization error')
    else:
        print(initialize_result[1])

    # Create batch for testing
    filename = test_filename
    journal_batch_name = test_journal_batch_name
    journal_batch_description = test_journal_batch_description
    journal_batch_entity = test_journal_batch_entity
    journal_batch_currency = test_journal_batch_currency
    gl_post_reference = test_gl_post_reference
    gl_batch_status = test_gl_batch_status

    insert_new_batch_name(journal_batch_name,
                          journal_batch_description,
                          str(journal_batch_entity),
                          str(journal_batch_currency),
                          gl_post_reference,
                          str(gl_batch_status),
                          )

    # Set up csv file to use
    print('=' * 80)
    batch_row_id = get_journal_batch_row_id_by_name(journal_batch_name)
    print(f'journal_batch_name: {journal_batch_name}')
    print(f'batch_row_id: {batch_row_id}')
    print(f'filename: {filename}')
    batch_row_id = batch_row_id[0][0][0]
    # batch_row_id = batch_row_id[0][0]  <<< use to test malformed query
    print(f'batch_row_id: {batch_row_id}')
    print('=' * 80)

    # Load csv file to journal_loader
    load_file = batch_load_je_file(filename, str(batch_row_id))
    print('=' * 80)

    print(f'load_file: {load_file}')

    print('=' * 80)
    if load_file == 'LOAD OKAY':
        status_ = 1
    else:
        status_ = 99
    assert(status_ == 1)

    # Compare csv totals loaded into pandas dataframe to journal
    # table totals.

    # Load batch in journal_loader to journal
    load_status_journal = batch_load_insert(batch_row_id)
    print('*' * 100)
    print(f'load_status_journal: {load_status_journal}')
    print('*' * 100)
    df = pd.read_csv(working_data_folder + filename)
    print(df.head())
    print(f'batch_row_id: {batch_row_id}')

    df_dr_total = df['journal_debit'].sum()
    df_cr_total = df['journal_credit'].sum()

    journal_txt, journal_DR_total, journal_CR_total = batch_total('journal', batch_row_id)

    assert(df_dr_total == round(journal_DR_total, 2))
    assert(df_cr_total == round(journal_CR_total, 2))


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

    print('+' * 60)
    print()
    check_status = test_csv_load_process()
    print(f'check_status: {check_status}')
    print('+' * 60)
    print()

    print('>' * 90)
    print()
    try:
        cnx = create_connection(**config)
        cursor = cnx.cursor()
        cursor.execute("SELECT * FORM employees")   # Syntax error in query
        cnx.close()
    except mysql.connector.Error as err:
        print(f'Something went wrong: {err}')
    print()
    print('<' * 90)
