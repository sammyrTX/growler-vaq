# queries_insert.py

"""SQL insert queries."""
import sys
import csv
import mysql
import mysql.connector
from mysql.connector.errors import Error

from .. db_config import config, working_data_folder

from .. db_connection import (create_connection,
                              execute_query,
                              execute_read_query,
                              )

# Valid status for the General Ledger posting process
# See insert_new_batch_name for a description.
valid_status = [0, 10, 20, 30, 40]


def insert_new_batch_name(journal_batch_name,
                          journal_batch_description,
                          journal_batch_entity,
                          journal_batch_currency,
                          gl_post_reference,
                          gl_batch_status,
                          ):
    """Insert new batch name into journal batch table.

    Batches used to group journal entries. Each batch will be
    associated with a unique entity and currency combination, i.e.,
    je's for a given batch will only be in one currency and associated
    with one entity.

    gl_batch_status will indicate which stage it is in the GL post process.
    Need to update the valid_status list when making any changes.

    CODE         STATUS
    ----         --------------------------
      0           New - Just created
     10           Journal Entries have been assigned to this batch
     20           Journal Entries have been posted to journal table
     30           Journal Entries have been aggregated and loaded into the
                  gl staging table
     40           gl staging data has been inserted into the general_ledger
                  table and batch is now considered posted to the gl
     99           load error
    """

    add_new_batch_id = """ INSERT INTO journal_batch (journal_batch_name,
     journal_batch_description, journal_batch_entity,
     journal_batch_currency, gl_post_reference, gl_batch_status)

    VALUES ('""" + journal_batch_name + """', '""" + journal_batch_description + """', """ + journal_batch_entity + """, """ + journal_batch_currency + """, '""" + gl_post_reference + """', """ + gl_batch_status + """);
    """
    connection = create_connection(**config)

    return execute_query(connection, add_new_batch_id)


def insert_new_je_transaction(journal_name,
                              journal_date,
                              account_number,
                              department_number,
                              journal_entry_type,
                              journal_debit,
                              journal_credit,
                              journal_description,
                              journal_reference,
                              journal_batch_id,
                              gl_post_reference,
                              journal_entity,
                              journal_currency,
                              ):
    """Insert new JE transaction into the journals table."""
    add_new_je = """INSERT INTO journals (journal_name,
                              journal_date,
                              account_number,
                              department_number,
                              journal_entry_type,
                              journal_debit,
                              journal_credit,
                              journal_description,
                              journal_reference,
                              journal_batch_id,
                              gl_post_reference,
                              journal_entity,
                              journal_currency)
                              VALUES ('""" + journal_name + """', '""" + journal_date + """', """ + str(account_number) + """, """ + str(department_number) + """, """ + str(journal_entry_type) + """, """ + str(journal_debit) + """, """ + str(journal_credit) + """, '""" + journal_description + """', '""" + journal_reference + """', '""" + journal_batch_id + """', '""" + gl_post_reference + """', """ + str(journal_entity) + """, """ + str(journal_currency) + """);"""
    connection = create_connection(**config)
    return execute_query(connection, add_new_je)


def insert_je_row(table,
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
                  ):
    # Insert a row of journal entry data into the table passed to the function
    try:
        connection = create_connection(**config)
        insert_into_table = """INSERT INTO """ + table + """(journal_date, account_number, department_number, journal_entry_type, journal_debit, journal_credit, journal_description, journal_reference, journal_batch_row_id, gl_post_reference, journal_entity, journal_currency) VALUES ('""" + journal_date + """', """ + str(account_number) + """, """ + str(department_number) + """, """ + str(journal_entry_type) + """, """ + str(journal_debit) + """, """ + str(journal_credit) + """, '""" + journal_description + """', '""" + journal_reference + """', '""" + str(journal_batch_row_id) + """', '""" + gl_post_reference + """', """ + str(journal_entity) + """, """ + str(journal_currency) + """);"""

        load_status = execute_query(connection, insert_into_table)

        if load_status == 'Query executed successfully':
            # Set to zero to indicate load was successful
            load_status = 0
            print(f"*** INSERT COMPLETE ***")
        else:
            # Set to 99 to indicate load error
            load_status = 99
            print(f'ERROR with Loader to Journals table')

        connection.close()
        return load_status

    except IndexError:
        print("IndexError!")
        return "INDEX ERROR"


def batch_load_je_file(filename, batch_row_id):

    """Load csv file provided into staging journal entries table (journal_loader) and validate before inserting into journals table
    """
    # Set load status flag
    load_status = 'PENDING'
    # Take passed filename argument and load into working table

    #  Open connection to database and open csv file to load
    try:
        connection = create_connection(**config)
        print(f"Successfully connected to ({config['database']})")
    except ConnectionError as error:
        print("Failed to connect ", error)

    #  Open csv file to load
    with open(working_data_folder + filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                je_row_insert_query = """INSERT INTO journal_loader(journal_date, account_number, department_number, journal_entry_type, journal_debit, journal_credit, journal_description, journal_reference, journal_batch_row_id, gl_post_reference, journal_entity, journal_currency) VALUES('""" + row[1] + """', """ + row[2] + """, """ + row[3] + """, """ + row[4] + """, """ + row[5] + """, """ + row[6] + """, '""" + row[7] + """', '""" + row[8] + """', """ + str(batch_row_id) + """, '""" + row[10] + """', """ + row[11] + """, """ + row[12] + """)"""

                result = execute_query(connection, je_row_insert_query)
                print(f'result: {result}')

                if result == 'Query executed successfully':
                    line_count += 1
                    print(f'line count: {line_count}')
                    load_status = 'LOAD OKAY'
                    print('+' * 100)
                else:
                    print(f'ERROR: {result}')
                    load_status = 'LOAD ERROR'
                    break

        connection.close()
    # finally:
    #     print(f"filename loaded to journal_loader: {filename}")
    print('>>>>>>')
    print(f'>>>>>> Load status: {load_status}')
    print('>>>>>>')

    if load_status == 'LOAD ERROR':
        update_batch_gl_status(batch_row_id, 99)
        print(f"Load Error...Filename: {filename}")
        return "LOAD ERROR"
    elif load_status == 'LOAD OKAY':
        update_batch_gl_status(batch_row_id, 10)
        print(f"Load function end...Filename: {filename}")
        return load_status
    else:
        update_batch_gl_status(batch_row_id, 98)
        print(f"Load Error other...Filename: {filename}")
        return "LOAD ERROR OTHER"


def update_batch_gl_status(batch_row_id, status):

    """In the journal_batch table, update the gl status of the batch row id to the passed status argument.
    """

    # Set the status argument to 99 if the argument is not valid
    if status not in valid_status:
        status = 99

    try:
        connection = create_connection(**config)
        update_gl_status = """UPDATE journal_batch SET gl_batch_status = """ + str(status) + """  WHERE journal_batch_row_id = """ + str(batch_row_id)

        execute_query(connection, update_gl_status)

        batch_status = "OK"
        print(f"*** journal batch gl status updated successfully ***")
        connection.close()
        return (batch_status)

    except IndexError:
        print("IndexError!")
        return "INDEX ERROR"


def batch_load_insert(batch_row_id):

    """load rows for a batch_row_id from journal_loader and insert into journals
    """

    try:
        connection = create_connection(**config)
        insert_loader_to_journal = """INSERT INTO journal(journal_date, account_number, department_number, journal_entry_type, journal_debit, journal_credit, journal_description, journal_reference, journal_batch_row_id, gl_post_reference, journal_entity, journal_currency) SELECT journal_date, account_number, department_number, journal_entry_type, journal_debit, journal_credit, journal_description, journal_reference, journal_batch_row_id, gl_post_reference, journal_entity, journal_currency FROM journal_loader
          WHERE journal_batch_row_id = """ + str(batch_row_id)

        execute_query(connection, insert_loader_to_journal)

        #  After loading journal table, delete rows from the loader table
        clear_journal_loader = """DELETE FROM journal_loader WHERE journal_batch_row_id = """ + str(batch_row_id)

        print(f'clear_journal_loader: {clear_journal_loader} <<<<<<<<<')
        execute_query(connection, clear_journal_loader)

        # Update batch status to "1"
        loader_to_journal_status = update_batch_gl_status(batch_row_id, 20)

        if loader_to_journal_status == 'OK':
            # Set to zero to indicate journal_loader to journal INSERT COMPLETE
            load_status = 0
            print(f"*** INSERT COMPLETE ***")
            connection.close()
        else:
            # Set to 99 to indicate and error with the load
            load_status = 99
            print(f'ERROR with Loader to Journals table')
            connection.close()
        return load_status

    except IndexError:
        print("IndexError!")
        return "INDEX ERROR"


if __name__ == "__main__":
    connection = create_connection(**config)

    # JE transaction load test
    # insert_new_je_transaction('Test JE',
    #                           '2020-07-13',
    #                           1111,
    #                           200,
    #                           1,
    #                           1000.99,
    #                           0.0,
    #                           'journal_description',
    #                           'journal_reference',
    #                           'journal_batch_id',
    #                           'gl_post_reference',
    #                           1,
    #                           1,
    #                           )

    # filename = 'je_load_kilo.csv'
    # batch_row_id = 2

    # batch_load_je_file(filename, batch_row_id)

    batch_row_id = 13

    batch_load_insert(batch_row_id)

    print(f'load complete...verify {batch_row_id} is in journal and deleted from journal_loader...')
