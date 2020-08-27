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

"""
Current READ queries:

def select_all(table):
def select_batch_available(table):
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


def test_query():
    table = 'chart_of_accounts'
    rows = select_all(table)
    # row_count = rows.count('\n')
    row_count = 0

    for _ in rows:
        row_count +=1

    assert(row_count > 0)


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
