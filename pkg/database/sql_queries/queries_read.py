# queries_read.py

"""
SQL read queries
"""

from .. db_connection import (create_connection,
                              execute_query,
                              execute_read_query,
                              )


def read_chart_of_accounts():
    """select all rows from the chart_of_accounts table"""

    webdev_pw = 'MtC^k632coW$c1qK5@Nh#NG$vpNiE*QX2$$6F#lbq9HYGCiVQA'
    connection = create_connection("localhost", "webdev", webdev_pw, "acctg_system")

    select_accts = "SELECT * FROM chart_of_accounts"

    return execute_read_query(connection, select_accts)
