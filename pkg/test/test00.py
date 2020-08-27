"""test file"""

import mysql.connector
# from mysql.connector import Error
# from . db_config import config


def func01():
    """Just return the int 42"""
    return 42


def func02():
    """Just return the string TESLA"""
    return 'TESLA'


def test_check00():
    int_value = int()
    int_value = func01()

    assert(int_value == 42)


def test_check02():
    test_str = str()
    test_str = func02()

    assert(test_str == 'TESLA')


if __name__ == '__main__':
    pass
