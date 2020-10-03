# queries_read.py

"""
SQL read queries
"""

from .. db_connection import (create_connection,
                              execute_query,
                              execute_read_query,
                              )

from .. db_config import config

import mysql.connector
from mysql.connector import Error


def select_all(table):
    """select all rows from a given table"""
    connection = create_connection(**config)

    select_accts = "SELECT * FROM " + table

    return execute_read_query(connection, select_accts)


def select_batch_available(table):
    """select all rows from journal_batch table that have not been posted
    to the journal table (i.e. batch status not equal to 20)."""
    connection = create_connection(**config)

    select_batch = """SELECT * FROM """ + table + """ WHERE gl_batch_status <> 20 ORDER BY journal_batch_row_id DESC;"""

    print(f'{select_batch}')

    return execute_read_query(connection, select_batch)


def select_batch_loaded(table):
    """Select all rows from journal_batch table that have been posted
    to the journal table.

    This is an inner join on journal_batch.journal_batch_row_id to journal table rows that have the same journal_batch_row_id. Include the total of debits and credits from the journal table. This query will select rows from journal table regardless of gl_batch_status (which should be 20 if posted to the journal table."""

    connection = create_connection(**config)

    select_batch = """SELECT b.journal_batch_row_id, b.journal_batch_name, b.journal_batch_description, j.journal_batch_row_id, sum(j.journal_debit) as DR, sum(j.journal_credit) as CR FROM journal j, """ + table + """ b WHERE j.journal_batch_row_id = b.journal_batch_row_id GROUP BY j.journal_batch_row_id ORDER BY j.journal_batch_row_id DESC"""

    print(f'{select_batch}')

    return execute_read_query(connection, select_batch)


def select_batch_by_row_id(table, journal_batch_row_id):
    """Select row(s) from a table for a specific batch based
    on journal_batch_row_id.
    """

    connection = create_connection(**config)

    print('******* in select_batch_by_row_id function **********')

    select_batch = """SELECT * FROM """ + table + """ WHERE journal_batch_row_id = """ + str(journal_batch_row_id) + """;"""

    print(f'select_batch: {select_batch}')
    return execute_read_query(connection, select_batch)


def select_rowcount_row_id(table, row_id):
    """Select count of rows from a table for a row_id.
    One use will be to check if there are any existing rows for a batch_row_id in the journal_loader_table"""

    # Set field depending on which table is being passed
    if table == 'journal_loader':
        row_field = 'journal_batch_row_id'
    elif table == 'journal':
        row_field = 'journal_row_id'
    elif table == 'journal_batch':
        row_field = 'journal_batch_row_id'
    else:
        row_field = 'table_not_found'

    connection = create_connection(**config)

    row_count = """SELECT count(*) FROM """ + table + """ WHERE """ + row_field + """ = """ + str(row_id) + """;"""

    row_count_result = execute_read_query(connection, row_count)

    return row_count_result[0][0]


def batch_total(table, batch_row_id):

    """For a given batch row id and table, total the debits and credits.
    """

    connection = create_connection(**config)

    dr_cr_totals_query = """SELECT journal_batch_row_id, sum(journal_debit), sum(journal_credit) FROM """ + table + """ WHERE journal_batch_row_id = '""" + str(batch_row_id) + """' GROUP BY journal_batch_row_id"""

    dr_cr_totals = execute_read_query(connection, dr_cr_totals_query)
    dr_cr_totals_list = list(dr_cr_totals)

    if dr_cr_totals is None:

        # Make DR != CR so HTML flags it as not ready to post to GL
        print("FUNC: batch_total >>> ERROR", 999999, 888888)
        return ("ERROR", 999999, 888888)

    try:
        print(f"FUNC: batch_total - journal_batch_row_id >>> {dr_cr_totals_list[0][0]}")
        print(f"FUNC: batch_total  - dr total >>> {dr_cr_totals_list[0][1]}")
        print(f"FUNC: batch_total - cr total >>> {dr_cr_totals_list[0][2]}")

        return (dr_cr_totals_list[0][0],
                dr_cr_totals_list[0][1],
                dr_cr_totals_list[0][2],
                )
    except IndexError:
        print("IndexError!")
        return ("INDEX ERROR",
                999999,
                888888,  #  Make different so flagged as not ready to post
                )

# Not being used, but keeping code for possible future use
# def select_entity_name_by_id(table, journal_batch_entity):
#     """Select the corresponding entity name for the given entity id from the
#     journal entry batch.
#     """

#     connection = create_connection(**config)

#     select_entity = """SELECT entity_name FROM """ + table + """ WHERE entity_id = """ + str(journal_batch_entity) + """;"""

#     return execute_read_query(connection, select_entity)

#     currency__ = Currency.query.filter_by(currency_id=batch_currency).first()

# Not being used, but keeping code for possible future use
# def select_entity_list():
#     """Select all the rows from the entity table and the corresponding
#     currency names from the currency table. This can be used to populate a
#     drop down table."""

#     connection = create_connection(**config)

#     select_all_entities = """SELECT e.*, c.currency_code FROM entity e, currency c WHERE e.currency_id = c.currency_id ORDER BY e.entity_id"""

#     return execute_read_query(connection, select_all_entities)


def get_gl_batch_status(journal_batch_row_id):
    connection = create_connection(**config)

    gl_batch_status = """SELECT gl_batch_status from journal_batch WHERE journal_batch_row_id = """ + str(journal_batch_row_id)

    gl_batch_status_check = execute_read_query(connection, gl_batch_status)

    if gl_batch_status_check is None:
        return (99, 'Error - No journal batch row id found')
    else:
        return (gl_batch_status, 'OK')


def get_journal_batch_row_id_by_name(journal_batch_name):
    """Get the journal_batch_row_id by journal_batch_name"""

    try:
        connection = create_connection(**config)

        row_id_qry = """SELECT journal_batch_row_id from journal_batch WHERE journal_batch_name = '""" + journal_batch_name + """'"""

        row_id_out = execute_read_query(connection, row_id_qry)

        if row_id_out is None:
            return (0, 'Error - No journal batch row id found')
        else:
            row_id = row_id_out[0][0]
            return (row_id_out, 'OK')
    except Error:
        print('*** ERROR ***')
        return (99, '*** Error***')
