import pandas as pd
import src.data_adapters as db


ACCOUNTS_FILE_FULL_PATH = db.ACCOUNTS_FILE
TRANSACTIONS_FILE_FULL_PATH = db.TRANSACTIONS_FILE

EMPTY_FILE_FULL_PATH = 'empty.csv'
ONLY_COLUMNS_FILE_FULL_PATH = 'only_columns.csv'


# def test_empty_data_file_read():
#     ret = True
#
#     try:
#         result: pd.DataFrame = db.DataLoader._read_file(EMPTY_FILE_FULL_PATH)
#     except pd.errors.DataError as ex:
#         print(f'\n{ex}')
#
#     assert ret


def test_only_columns_data_file_read():
    try:
        result: pd.DataFrame = db.DataLoader._read_file(ONLY_COLUMNS_FILE_FULL_PATH)
    except Exception as ex:
        print(ex)

    assert result is not None


def test_accounts_data_file_read():
    result: pd.DataFrame = db.DataLoader._read_file(ACCOUNTS_FILE_FULL_PATH)
    assert result is not None


def test_transactions_data_file_read():
    result: pd.DataFrame = db.DataLoader._read_file(TRANSACTIONS_FILE_FULL_PATH)
    assert result is not None
