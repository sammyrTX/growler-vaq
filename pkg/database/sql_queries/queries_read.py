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
    """select all rows from table"""
    connection = create_connection(**config)

    select_accts = "SELECT * FROM " + table

    return execute_read_query(connection, select_accts)
