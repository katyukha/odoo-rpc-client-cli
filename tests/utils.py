import os


def get_connection_str():
    return os.environ.get('TEST_CONNECTION_STR')
