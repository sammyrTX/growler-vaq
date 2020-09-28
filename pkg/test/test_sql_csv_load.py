# test_sql_csv_load.py

"""Test csv load process

    Test journal entry csv file load process by running the sql functions
    utilized by the front end. Check the total of the debit and credit amounts
    loaded into the journal table against a pandas dataframe of the csv file
    to confirm they tie.

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
                                                  # select_je_by_row_id,
                                                  select_rowcount_row_id,
                                                  select_batch_id,
                                                  batch_total,
                                                  select_entity_name_by_id,
                                                  select_entity_list,
                                                  get_gl_batch_status,
                                                  batch_total,
                                                  get_journal_batch_row_id_by_name,
                                                  )

from .. database.sql_queries.queries_insert import (batch_load_je_file,
                                                    insert_new_batch_name,
                                                    batch_load_insert,
                                                    )

from . test_queries import query_initialize_000

import pandas as pd

# Values to be used within scope of test_sql_csv_load.py
test_filename = 'csv_out02.csv'
test_journal_batch_name = 'pytest-test_csv_load101'
test_journal_batch_description = 'csv_out02.csv'
test_journal_batch_entity = 1
test_journal_batch_currency = 1
test_gl_post_reference = 'NULL'
test_gl_batch_status = 0


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
    batch_row_id = get_journal_batch_row_id_by_name(journal_batch_name)
    print(f'journal_batch_name: {journal_batch_name}')
    print(f'batch_row_id raw: {batch_row_id}')
    print(f'filename: {filename}')
    batch_row_id = batch_row_id[0][0][0]
    # batch_row_id = batch_row_id[0][0]  <<< use to test malformed query
    print(f'batch_row_id: {batch_row_id}')

    # Load csv file to journal_loader
    load_file = batch_load_je_file(filename, str(batch_row_id))
    print(f'load_file: {load_file}')

    if load_file == 'LOAD OKAY':
        status_ = 1
    else:
        status_ = 99
    assert(status_ == 1)

    # Compare csv totals loaded into pandas dataframe to journal
    # table totals.

    # Load batch in journal_loader to journal
    load_status_journal = batch_load_insert(batch_row_id)
    print(f'load_status_journal: {load_status_journal}')

    # Load csv file inro pandas dataframe
    df = pd.read_csv(working_data_folder + filename)
    print(df.head())
    print(f'batch_row_id: {batch_row_id}')

    # Get DR/CR totals in dataframe
    df_dr_total = df['journal_debit'].sum()
    df_cr_total = df['journal_credit'].sum()

    journal_txt, journal_DR_total, journal_CR_total = batch_total('journal', batch_row_id)
    print('-' * 100)
    print()

    print(f'journal_txt: {journal_txt}')
    print(f'journal_DR_total: {journal_DR_total}')
    print(f'journal_CR_total: {journal_CR_total}')

    print()
    print('-' * 100)
    assert(df_dr_total == round(journal_DR_total, 2))
    assert(df_cr_total == round(journal_CR_total, 2))

    if __name__ == '__main__':

        """Test samples"""

        def sample_test():
            pass
