# queries_insert.py

"""SQL insert queries."""
import mysql.connector
from mysql.connector import Error
from .. db_config import config

from .. db_connection import (create_connection,
                              execute_query,
                              execute_read_query,
                              )


def select_all(table):
    """Select all rows from table."""
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
    """Insert new batch id into journal batch table.

    Batches used to group journal entries. Each batch will be
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
    print('*' * 50)
    print(f'{journal_batch_id} >>> type: {type(journal_batch_id)}')
    print(f'{journal_batch_description} >>> type: {type(journal_batch_description)}')
    print(f'{journal_batch_entity} >>> type: {type(journal_batch_entity)}')
    print(f'{journal_batch_currency} >>> type: {type(journal_batch_currency)}')
    print(f'{gl_post_reference} >>> type: {type(gl_post_reference)}')
    print(f'{gl_batch_status} >>> type: {type(gl_batch_status)}')
    print('*' * 50)

    add_new_batch_id = """ INSERT INTO journal_batch (journal_batch_id,
     journal_batch_description, journal_batch_entity,
     journal_batch_currency, gl_post_reference, gl_batch_status)

    VALUES ('""" + journal_batch_id + """', '""" + journal_batch_description + """', """ + journal_batch_entity + """, """ + journal_batch_currency + """, '""" + gl_post_reference + """', """ + gl_batch_status + """);
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


# ****** >>>> Resume Here <<<<<<<<< **********
#
# Refactor function to enable it to use the mariadb infrastructure
#
#

def batch_load_je_file(filename):

    """Load csv file provided into staging journal entries table (journals_load) and validate before inserting into journals table
    """

    # Take passed filename argument and load into working table

    #  Open connection to database and open csv file to load
    try:
        sqliteConnection = sqlite3.connect(database_folder + db_name)
        cursor = sqliteConnection.cursor()
        print(f"Successfully connected to SQLite ({db_name})")



        with open(working_data_folder + filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    sqlite_insert_query = """INSERT INTO journals_loader(journal_name, journal_date, account_number, department_number, journal_entry_type, journal_debit, journal_credit, journal_description, journal_reference, journal_batch_id, gl_post_reference, journal_entity, journal_currency) VALUES('""" + row[1] + """', '""" + row[2] + """', """ + row[3] + """, """ + row[4] + """, """ + row[5] + """, """ + row[6] + """, """ + row[7] + """, '""" + row[8] + """', '""" + row[9] + """', '""" + row[10] + """', '""" + row[11] + """', """ + row[12] + """, """ + row[13] + """)"""

                    cursor.execute(sqlite_insert_query)
                    line_count += 1

            sqliteConnection.commit()
            print(f"rows inserted: {line_count}")
            cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into SQLite table", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
        print(f"filename passed: {filename}")

    print(f"Load function end...Filename: {filename}")
    return "LOAD OK"


if __name__ == "__main__":
    connection = create_connection(**config)

    insert_new_je_transaction('Test JE',
                              '2020-07-13',
                              1111,
                              200,
                              1,
                              1000.99,
                              0.0,
                              'journal_description',
                              'journal_reference',
                              'journal_batch_id',
                              'gl_post_reference',
                              1,
                              1,
                              )
