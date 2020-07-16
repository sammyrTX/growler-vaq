# queries_read.py

"""
SQL read queries
"""

from .. db_connection import (create_connection,
                              execute_query,
                              execute_read_query,
                              )

from .. db_config import config


def select_all(table):
    """select all rows from a given table"""
    connection = create_connection(**config)

    select_accts = "SELECT * FROM " + table

    return execute_read_query(connection, select_accts)


def select_batch_available(table):
    """select all rows from journal_batch table that have not been posted
    to the General Ledger (i.e. batch status not equal to 3)."""
    connection = create_connection(**config)

    select_batch = """SELECT * FROM """ + table + """ WHERE gl_batch_status <> 3 ORDER BY journal_batch_row_id DESC;"""

    print(f'{select_batch}')

    return execute_read_query(connection, select_batch)


def select_batch_by_id(table, journal_batch_row_id):
    """Select a row from journal_batch for a specific batch joining
    on journal_batch_row_id."""

    connection = create_connection(**config)

    select_batch = """SELECT * FROM """ + table + """ WHERE journal_batch_row_id = """ + str(journal_batch_row_id) + """;"""

    return execute_read_query(connection, select_batch)


def select_entity_name_by_id(table, journal_batch_entity):
    """Select the corresponding entity name for the given entity id from the
    journal entry batch.
    """

    connection = create_connection(**config)

    select_entity = """SELECT entity_name FROM """ + table + """ WHERE entity_id = """ + str(journal_batch_entity) + """;"""

    return execute_read_query(connection, select_entity)

    currency__ = Currency.query.filter_by(currency_id=batch_currency).first()

