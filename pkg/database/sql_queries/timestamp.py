# timestamp.py

"""Functions to generate a timestamp based on UTC. It will be in the form
of a string.
"""

import datetime


def timestamp_generator():
    """Using UTC date & time, generate a string that will be a timestamp
    """

    utc_string = str(datetime.datetime.utcnow())

    year_ = utc_string[0:4]
    month_ = utc_string[5:7]
    day_ = utc_string[8:10]
    zulu_ = utc_string[11:]

    timestamp = year_ + month_ + day_ + "-" + zulu_

    # print(f"timestamp: {timestamp}")  # remove comment if needed for testing

    return timestamp


def timestamp_session():
    """Create a set of timestamps at a given instance with various formats to be utilized with insert processes.
    """

    # Generate time and date stamp for insert

    timestamp_raw = timestamp_generator()
    timestamp_gl = 'GL' + timestamp_raw
    timestamp_gls = 'GLS' + timestamp_raw
    timestamp_je = 'JE' + timestamp_raw
    timestamp_ = timestamp_raw[0:8]
    datestamp_ = timestamp_[0:4] + "-" + timestamp_[4:6] + "-" + timestamp_[6:8]

    return (timestamp_raw,
            timestamp_gl,
            timestamp_je,
            timestamp_,
            datestamp_,
            timestamp_gls,
            )


if __name__ == '__main__':

    """Test output of timestamp functions"""

    print(f'*** BEGIN ***')
    print(f'timestamp: {timestamp_generator()}')
    print(f'*** END ***')
    print()
    print(f'*** BEGIN ***')

    session_ = timestamp_session()

    for _ in session_:
        print(f'{_}')

    print('-' * 20)
    print(f'timestamp: {timestamp_session()}')
    print('-' * 20)

    print(f'*** END ***')
