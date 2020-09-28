# test_queries.py

"""Queries for testing processes

    **** NOT FOR PRODUCTION USE ****

    Some queries in this module will alter table data and should only be used
    during testing.
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

# List of sample batches in a dict that can be loaded into journal_batch

test_sample_batches = [{'journal_batch_name': 'test_batch_000',
                        'journal_batch_description': 'test_batch_000_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_001',
                        'journal_batch_description': 'test_batch_001_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_002',
                        'journal_batch_description': 'test_batch_002_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_003',
                        'journal_batch_description': 'test_batch_003_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_004',
                        'journal_batch_description': 'test_batch_004_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_005',
                        'journal_batch_description': 'test_batch_005_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_006',
                        'journal_batch_description': 'test_batch_006_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_007',
                        'journal_batch_description': 'test_batch_007_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_008',
                        'journal_batch_description': 'test_batch_008_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       ]

test_sample_batch00 = [{'journal_batch_name': 'test_batch_100',
                        'journal_batch_description': 'test_batch_000_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_101',
                        'journal_batch_description': 'test_batch_001_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       {'journal_batch_name': 'test_batch_102',
                        'journal_batch_description': 'test_batch_002_d',
                        'journal_batch_entity': '1',
                        'journal_batch_currency': '1',
                        'gl_post_reference': 'NULL',
                        'gl_batch_status': '0',
                        },
                       ]

test_sample_batch01 = [{'journal_date': '2019-3-10',
                        'account_number': '4210',
                        'department_number': '200',
                        'journal_entry_type': 'NULL',
                        'journal_debit': '400.50',
                        'journal_credit': '0.0',
                        'journal_description': 'test_batch_000_d',
                        'journal_reference': 'ref ',
                        'journal_batch_row_id': '0',
                        'gl_post_reference': '*BLANK*',
                        'journal_entity': '1',
                        'journal_currency': '1',
                        },
                        {'journal_date': '2019-3-10',
                        'account_number': '5100',
                        'department_number': '300',
                        'journal_entry_type': 'NULL',
                        'journal_debit': '0.00',
                        'journal_credit': '6547.99',
                        'journal_description': 'test_batch_000_d',
                        'journal_reference': 'ref ',
                        'journal_batch_row_id': '0',
                        'gl_post_reference': '*BLANK*',
                        'journal_entity': '1',
                        'journal_currency': '1',
                        },
                        {'journal_date': '2019-3-10',
                        'account_number': '6060',
                        'department_number': '110',
                        'journal_entry_type': 'NULL',
                        'journal_debit': '0.0',
                        'journal_credit': '3300.50',
                        'journal_description': 'test_batch_000_d',
                        'journal_reference': 'ref ',
                        'journal_batch_row_id': '0',
                        'gl_post_reference': '*BLANK*',
                        'journal_entity': '1',
                        'journal_currency': '1',
                        },
                       ]


def query_initialize_000(table_list):
    """Delete all rows in each table that is passed in the list argument"""

    # Iterate through each table in the list and delete all rows

    connection = create_connection(**config)
    delete_status = 0  # Default as zero for no error; 99 if there is an error.
    for _ in table_list:
        delete_all_rows = """DELETE FROM """ + _
        _delete = execute_query(connection, delete_all_rows)

        if _delete == 'Query executed successfully':
            delete_status = 0
            continue
        else:
            print(f'Delete failed: {_delete}')
            delete_status = 99
            break

    connection.close()
    return [delete_status, f'Delete process completed ({_delete})']


def load_csv_to_journal(batch_info):
    """Take a dict of batch and csv info and load into journal table."""

    # Create batch for testing
    filename = batch_info['filename']
    journal_batch_name = batch_info['journal_batch_name']
    journal_batch_description = batch_info['journal_batch_description']
    journal_batch_entity = batch_info['journal_batch_entity']
    journal_batch_currency = batch_info['journal_batch_currency']
    gl_post_reference = batch_info['gl_post_reference']
    gl_batch_status = batch_info['gl_batch_status']

    insert_new_batch_name(journal_batch_name,
                          journal_batch_description,
                          str(journal_batch_entity),
                          str(journal_batch_currency),
                          gl_post_reference,
                          str(gl_batch_status),
                          )

    # Set up csv file to use
    batch_row_id = get_journal_batch_row_id_by_name(journal_batch_name)
    batch_row_id = batch_row_id[0][0][0]

    # Load csv file to journal_loader
    load_file = batch_load_je_file(filename, str(batch_row_id))

    status_ = [0, batch_row_id]  # [load_file status, batch_row_id]

    if load_file == 'LOAD OKAY':
        status_[0] = 0
    else:
        status_[0] = 99
        raise Exception('Error posting csv file to Journal table')

    # Compare csv totals loaded into pandas dataframe to journal
    # table totals.

    # Load batch in journal_loader to journal
    if status_[0] == 0:
        load_status_journal = batch_load_insert(batch_row_id)
        print(f'load_status_journal: {load_status_journal}')
        return status_
    else:
        print(f'Error loading to journal_loader: {status_}')
        raise Exception('Error posting csv file to journal_loader')
        return status_


def get_batch_row_id_in_journal(batch_row_id):
    """Get journal_batch_row_id's and associated DR/CR totals"""
    print(f'batch_row_id arg: {batch_row_id}')

    try:
        connection = create_connection(**config)
        batches_in_journal = """SELECT journal_batch_row_id, sum(journal_debit) as total_dr, sum(journal_credit) as total_cr FROM journal GROUP BY journal_batch_row_id"""
        print(f'batches_in_journal: {batches_in_journal}')

        batches_loaded = execute_read_query(connection, batches_in_journal)
        print(f'batches: {batches_loaded}')
        connection.close()
        return batches_loaded
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return e


if __name__ == '__main__':

    # Begin table initialization

    table_list = ['journal_batch',
                  'journal_loader',
                  'journal'
                  ]

    _result = query_initialize_000(table_list)

    print(f'>>>> {_result}')
