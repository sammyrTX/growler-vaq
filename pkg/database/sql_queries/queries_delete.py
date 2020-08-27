# queries_update.py

"""SQL update queries."""
import mysql.connector

from mysql.connector import Error

from .. db_config import config, working_data_folder

from .. db_connection import (create_connection,
                              execute_query,
                              execute_read_query,
                              )

from . queries_read import get_gl_batch_status


def delete_journal_batch(journal_batch_row_id):
    pass
    """Delete a journal batch for a given journal_batch_row_id."""
    """ """
    """This deletes the following:
          - Any corresponding rows from journal_loader.
          - Row from journal_batch for the journal_batch_row_id

        Exclude any batch id's that have a gl_batch_status value of 20.
        They have been posted the journal table and should be reversed using
        JE's."""

    # Check gl_batch_status before deleting
    get_gl_batch_status_value = get_gl_batch_status(journal_batch_row_id)

    print()
    print('=' * 80)

    print(f'get_gl_batch_status_value: {get_gl_batch_status_value}')
    print(f'journal_batch_row_id: {journal_batch_row_id}')

    print('=' * 80)
    print()

    if get_gl_batch_status_value != 20:

        connection = create_connection(**config)

        # Delete rows from journal_loader
        delete_rows_journal_loader = """DELETE FROM journal_loader WHERE journal_batch_row_id = """ + str(journal_batch_row_id)
        execute_query(connection, delete_rows_journal_loader)

        # Delete row from journal_batch
        delete_row_journal_batch = """DELETE FROM journal_batch WHERE journal_batch_row_id = """ + str(journal_batch_row_id)
        execute_query(connection, delete_row_journal_batch)

        return 'Batch Deleted'
    else:
        return 'Invalid Batch'


def je_transaction_updatex(_je_list):  # Remove when ready
    """Update JE transaction in journal_loader table."""

    # Unpack JE transaction
    (journal_loader_id,
    journal_date,
    account_number,
    department_number,
    journal_entry_type,
    journal_debit,
    journal_credit,
    journal_description,
    journal_reference,
    journal_batch_row_id,
    gl_post_reference,
    journal_entity,
    journal_currency,
    ) = _je_list

    update_je = """UPDATE journal_loader
    SET journal_date = '""" + journal_date + """',
    account_number = """ + str(account_number) + """,
    department_number = """ + str(department_number) + """,
    journal_entry_type = """ + str(journal_entry_type) + """,
    journal_debit = """ + str(journal_debit) + """,
    journal_credit = """ + str(journal_credit) + """,
    journal_description = '""" + str(journal_description) + """',
    journal_reference = '""" + str(journal_reference) + """',
    journal_batch_row_id = """ + str(journal_batch_row_id) + """,
    gl_post_reference = '""" + str(gl_post_reference) + """',
    journal_entity = """ + str(journal_entity) + """,
    journal_currency = """ + str(journal_currency) + """
    WHERE journal_loader_id = """ + str(journal_loader_id)

    connection = create_connection(**config)
    return execute_query(connection, update_je)


if __name__ == "__main__":
    connection = create_connection(**config)

    print('__main__')
    # _je_list = [229, '2019-11-01', 6070, 500, 99, 700.0, 0.0, 'test transaction v2 – expense-00', 'ref ***UPDATE***', 8, '', 1, 1]

    # je_transaction_update(_je_list)
