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

from . test_queries import (query_initialize_000,
                            load_csv_to_journal,
                            get_batch_row_id_in_journal,
                            )

import pandas as pd

"""
Current READ queries:

x def select_all(table):
def select_batch_available(table):
WIP def select_batch_loaded(table):
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


# ******* Resume HERE *******
# Need to add assert checks and any other intermediate steps
# Currently able to post csv's to journal table and now need to confirm
# that select_batch_loaded(table) is working as designed.

def test_select_batch_loaded_not_ready():
    """Check if select_batch_loaded function is gathering batches that have associated journal table rows.
    """

    # select_batch_loaded(table)

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
        print(f'initialization: {initialize_result[1]}')

    # Process batches and csv file data through journal load stage.

    # List of batch name(s) to use
    batch_names = ['check000',
                   'check001',
                   ]

    batch_info_00 = dict()
    batch_info_01 = dict()

    # First batch attributes
    batch_info_00['filename'] = 'je_load_kilo.csv'
    batch_info_00['journal_batch_name'] = batch_names[0]
    batch_info_00['journal_batch_description'] = 'je_load_kilo.csv'
    batch_info_00['journal_batch_entity'] = 1
    batch_info_00['journal_batch_currency'] = 1
    batch_info_00['gl_post_reference'] = 'NULL'
    batch_info_00['gl_batch_status'] = 0

    # Second batch attributes
    batch_info_01['filename'] = 'je_load_juliet.csv'
    batch_info_01['journal_batch_name'] = batch_names[1]
    batch_info_01['journal_batch_description'] = 'je_load_juliet.csv'
    batch_info_01['journal_batch_entity'] = 1
    batch_info_01['journal_batch_currency'] = 1
    batch_info_01['gl_post_reference'] = 'NULL'
    batch_info_01['gl_batch_status'] = 0

    # # Second batch attributes
    # batch_info_01['filename'] = 'csv_out01.csv'
    # batch_info_01['journal_batch_name'] = batch_names[1]
    # batch_info_01['journal_batch_description'] = 'csv_out01.csv'
    # batch_info_01['journal_batch_entity'] = 1
    # batch_info_01['journal_batch_currency'] = 1
    # batch_info_01['gl_post_reference'] = 'NULL'
    # batch_info_01['gl_batch_status'] = 0

    batch_info_00_out = load_csv_to_journal(batch_info_00)
    batch_info_01_out = load_csv_to_journal(batch_info_01)
    print(f'batch_info_00_out: {batch_info_00_out}')
    print(f'batch_info_01_out: {batch_info_01_out}')

    # Loaded batches that should be in journal table
    batches_loaded = [batch_info_00_out[1],
                      batch_info_01_out[1],
                      ]

    print(f'batches_loaded: {batches_loaded} <<<<<')

    if batch_info_00_out[0] == 0 and batch_info_01_out[0] == 0:
        #Check if batches have corresponding rows in the journal table
        print(f'&&&&&&&&&&&&&&&&&&&&')
        batch_row_id = batches_loaded[0]
        print(f'batch_row_id ::: {batch_row_id}')

        #**** PROBLEM IS HERE ****
        batches_in_journal = get_batch_row_id_in_journal(batch_row_id)

        print(f'{batches_in_journal}')
        # for _ in batches_loaded:
        # raise Exception('Halt...!')

    else:
        # Raise exception if the status from load_csv_to_journal is not
        # zero for either batch.
        raise Exception('Error in csv to journal load process')



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
