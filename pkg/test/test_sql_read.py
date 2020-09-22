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
                            test_sample_batches,
                            )

import pandas as pd

"""
Current READ queries:

*** def select_all(table):
*** def select_batch_loaded(table):
*** def select_batch_available(table):
*** def select_batch_by_row_id(table, journal_batch_row_id):
*** def select_je_by_row_id(table, row_id): (*deleted, not being used*)

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


def test_select_all():
    """Check row count from select_all function"""

    table = 'z_test_table_00'
    test_row_0 = (1, 'sample', 11.99)
    rows = select_all(table)
    rows_count = len(rows)
    test_value = 6

    assert(rows_count == test_value)
    assert(rows[0] == test_row_0)


def test_select_batch_available():
    """Check batches that should be available. gl_batch_status should
       not equal 20."""

    # Clear journal_batch table
    table_list = ['journal_batch']
    delete_status = query_initialize_000(table_list)
    if delete_status[0] == 0:
        print('table initialization completed successfully')
    else:
        raise Exception(f'initialization of {table_list} failed')

    # Create test batches
    test_batch_name = [['batch000', 20],
                       ['batch001', 20],
                       ['batch002', 0],
                       ['batch003', 20],
                       ['batch004', 0],
                       ['batch005', 99],
                       ]

    batch_info = dict()

    for _ in test_batch_name:
        batch_info['journal_batch_name'] = _[0]
        batch_info['journal_batch_description'] = _[0] + ' - No csv file'
        batch_info['journal_batch_entity'] = '1'
        batch_info['journal_batch_currency'] = '1'
        batch_info['gl_post_reference'] = 'NULL'
        batch_info['gl_batch_status'] = str(_[1])

        insert_new_batch_name(**batch_info)

    # Put batch row id's that are not a status of 20 in a list
    test_batch_avail = list()

    for _ in test_batch_name:
        if _[1] != 20:
            row_ = get_journal_batch_row_id_by_name(_[0])
            test_batch_avail.append(row_[0][0][0])

    # Execute select_batch_available; put batch row id's in a list
    table = 'journal_batch'
    available_batches = select_batch_available(table)

    available_batches_row_ids = list()

    for _ in available_batches:
        available_batches_row_ids.append(_[0])

    # Test result set
    assert(test_batch_avail.sort() == available_batches_row_ids.sort())


def test_select_batch_loaded():
    """Check if select_batch_loaded function is gathering batches that have associated journal table rows.
    """

    # Initialize journal_batch, journal_loader and journal by deleting all
    # rows from each table

    table_list = ['journal_batch',
                  'journal_loader',
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

    csv_files = ['je_load_kilo.csv',
                 'je_load_kilo.csv',
                 ]

    batches_loaded = list()

    for idx, _ in enumerate(batch_names):
        batch_info = dict()

        batch_info['filename'] = csv_files[idx]
        batch_info['journal_batch_name'] = _
        batch_info['journal_batch_description'] = csv_files[idx]
        batch_info['journal_batch_entity'] = 1
        batch_info['journal_batch_currency'] = 1
        batch_info['gl_post_reference'] = 'NULL'
        batch_info['gl_batch_status'] = 0

        batch_info_out = load_csv_to_journal(batch_info)
        print(f'batch_info_out: {batch_info_out}')
        batches_loaded.append(batch_info_out)

    # Confirm each csv loaded is okay

    batches_loaded_status = 0
    batches_loaded_check = list()

    for _ in batches_loaded:
        if _[0] == 0:
            batches_loaded_status = 0
            batches_loaded_check.append(_[1])
        else:
            batches_loaded_status = 99

    if batches_loaded_status == 0:
        #Check if batches have corresponding rows in the journal table

        batch_row_id = batches_loaded[0]
        print(f'batch_row_id ::: {batch_row_id}')

        batches_in_journal = get_batch_row_id_in_journal(batch_row_id)
        batches_in_journal_check = [batches_in_journal[0][0], batches_in_journal[1][0]]

        assert(batches_loaded_check == batches_in_journal_check)

    else:
        # Raise exception if the status from load_csv_to_journal is not
        # zero for either batch.
        raise Exception('Error in csv to journal load process')


def test_select_batch_by_row_id():
    # Initialize journal_batch table before inserting sample rows
    table_list = ['journal_batch']
    delete_status = query_initialize_000(table_list)
    if delete_status[0] != 0:
        raise Error('Table initialization failed at test_select_batch_by_row_id()')

    # Load journal_batch with sample data dictionary from test_queries
    for _ in test_sample_batches:
        insert_new_batch_name(**_)

    # Use an arbitrary batch name from the sample batches loaded to get the
    # batch row id.

    journal_batch_name = test_sample_batches[3]['journal_batch_name']

    batch_row_id = get_journal_batch_row_id_by_name(journal_batch_name)

    if batch_row_id[1] != 'OK':
        raise Error('*** ERROR: test_select_batch_by_row_id not finding name')

    # Put contents of test sample batch from dict into a list for later assert
    test_sample_batch_to_check = list()
    test_sample_batch_to_check.append(batch_row_id[0][0][0])

    for key in test_sample_batches[3]:
        test_sample_batch_to_check.append(test_sample_batches[3][key])

    # Convert entity, currency & batch status to int
    test_sample_batch_to_check[3] = int(test_sample_batch_to_check[3])
    test_sample_batch_to_check[4] = int(test_sample_batch_to_check[4])
    test_sample_batch_to_check[6] = int(test_sample_batch_to_check[6])

    # Call select_batch_by_row_id and store result set
    table = 'journal_batch'
    journal_batch_row_id = batch_row_id[0][0][0]
    function_result = select_batch_by_row_id(table, journal_batch_row_id)

    # Compare sample data to function result set
    assert(test_sample_batch_to_check == list(function_result[0]))


def test_select_rowcount_row_id():
    pass
    # populate test table with data

    # call select_rowcount_row_id function

    # Compare sample data to function result set
    assert(test_sample_batch_to_check == list(function_result[0]))

    # >>> select_rowcount_row_id(table, row_id)


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
