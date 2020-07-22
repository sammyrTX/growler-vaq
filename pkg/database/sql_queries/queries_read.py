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


def select_batch_by_row_id(table, journal_batch_row_id):
    """Select row(s) from a table for a specific batch joining
    on journal_batch_row_id."""

    connection = create_connection(**config)

    print('******* in select_batch_by_id function **********')

    select_batch = """SELECT * FROM """ + table + """ WHERE journal_batch_row_id = """ + str(journal_batch_row_id) + """;"""

    return execute_read_query(connection, select_batch)


def select_je_by_row_id(table, journal_row_id):
    """Select row(s) from a table for a specific je joining
    on journal_row_id."""

    connection = create_connection(**config)

    select_je = """SELECT * FROM """ + table + """ WHERE journal_row_id = """ + str(journal_row_id) + """;"""

    return execute_read_query(connection, select_je)


def select_batch_id(table, journal_batch_row_id):
    """**** REVIEW  - May not need this function **** Get the batch_id from a journal table. One use is to obtain
    the batch id for transactions loaded into the journals_loader table."""

    connection = create_connection(**config)

    select_batch_id = """SELECT journal_batch_id FROM """ + table + """ GROUP BY journal_batch_id;"""

    return execute_read_query(connection, select_batch_id)


def batch_total(batch_row_id):

    """For a given batch, total the debits and credits
    """

    connection = create_connection(**config)

    dr_cr_totals_query = """SELECT journal_batch_row_id, sum(journal_debit), sum(journal_credit) FROM journal WHERE journal_batch_row_id = '""" + str(batch_row_id) + """' GROUP BY journal_batch_row_id"""

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


def select_entity_name_by_id(table, journal_batch_entity):
    """Select the corresponding entity name for the given entity id from the
    journal entry batch.
    """

    connection = create_connection(**config)

    select_entity = """SELECT entity_name FROM """ + table + """ WHERE entity_id = """ + str(journal_batch_entity) + """;"""

    return execute_read_query(connection, select_entity)

    currency__ = Currency.query.filter_by(currency_id=batch_currency).first()

