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


def query_initialize_000(table_list):
    """Delete all rows in each table that is passed in the list argument"""

    # Iterate through each table in the list and delete all rows

    connection = create_connection(**config)
    delete_status = 0 # Default as zero for no error; 99 if there is an error.

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

    return [delete_status, f'Delete process completed ({_delete})']


if __name__ == '__main__':

    # Begin table initialization

    table_list = ['journal_batch',
                  'journal_loader',
                  'journal'
                  ]

    _result = query_initialize_000(table_list)

    print(f'>>>> {_result}')
