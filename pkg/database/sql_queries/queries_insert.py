# queries_insert.py

"""
SQL insert queries
"""

from .. db_connection import (create_connection,
                              execute_query,
                              execute_read_query,
                              )

from .. db_config import config


def select_all(table):
    """select all rows from table"""
    connection = create_connection(**config)

    select_accts = "SELECT * FROM " + table

    return execute_read_query(connection, select_accts)


def insert_new_batch_id(journal_batch_id,
                        journal_batch_description,
                        journal_batch_entity,
                        journal_batch_currency,
                        gl_post_reference,
                        gl_batch_status,
                        ):

    """Insert new batch id into journal batch table"""

    """Batches used to group journal entries. Each batch will be
    associated with a unique entity and currency combination, i.e.,
    je's for a given batch will only be in one currency and associated
    with one entity.

    gl_batch_status will indicate which stage it is in the GL post process.

    CODE         STATUS
    ----         --------------------------
     0           New - Just created
     1           Journal Entries have been assigned to this batch
     2           Journal Entries have been aggregated and loaded into the
                 gl staging table
     3           gl staging data has been inserted into the general_ledger
                 table and batch is now considered posted to the gl
    """

    add_new_batch_id = """
INSERT INTO journal_batch (journal_batch_id, journal_batch_description, journal_batch_entity, journal_batch_currency, gl_post_reference, gl_batch_status)

VALUES ('""" + journal_batch_id + """', '""" + journal_batch_description + """', """ + journal_batch_entity + """, """ + journal_batch_currency + """, '""" + gl_post_reference + """', """ + gl_batch_status + """);
"""
    connection = create_connection(**config)

    return execute_query(connection, add_new_batch_id)
