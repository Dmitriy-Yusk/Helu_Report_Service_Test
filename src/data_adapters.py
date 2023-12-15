import os
from pathlib import Path
import pandas as pd
import threading
import logging
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import Session, sessionmaker

# import src.models as models
from src.models import AppTables, TransactionModelColumns
from src.utils import log_function_call
import src.config as cfg


logger = logging.getLogger(cfg.LOGGER_NAME)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = os.path.join(BASE_DIR, 'data')

DB_DATA_FULL_PATH = os.path.join(DATA_FOLDER, 'data.db')

ACCOUNTS_FILE = 'chart-of-accounts.csv'
TRANSACTIONS_FILE = 'bookings.csv'


class SQLEngine:
    _engine: Engine = None
    _session: Session = None

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            # cls._instance = super().__new__(cls)
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get(cls) -> Engine:
        return cls._instance._engine

    @classmethod
    def get_session(cls) -> Session:
        return cls._instance._session()

    @classmethod
    def init(cls):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
        # engine = create_engine(f'sqlite+pysqlite:///{DB_DATA_FULL_PATH}', echo=False)
        cls._instance._set(engine)

    @classmethod
    def _set(cls, engine: Engine):
        cls._instance._engine = engine
        cls._instance._session = sessionmaker(bind=engine)

    @classmethod
    def clear(cls):
        cls._instance._engine = None
        cls._instance._session = None


SQLEngine()


class DataLoader:
    """
    A class responsible for initial data loading from CSV files and load the data into SQLite in-memory DB
    """
    @classmethod
    @log_function_call
    def load(cls,
             engine: SQLEngine() = None,
             acc_file: str = ACCOUNTS_FILE,
             trans_file: str = TRANSACTIONS_FILE) -> None:
        if engine.get() is not None:
            return

        engine.init()
        sql_engine = engine.get()

        accounts, transactions = cls._load_csv_data(acc_file, trans_file)

        accounts.to_sql(AppTables.ACCOUNT, sql_engine, index=True)
        transactions.to_sql(AppTables.TRANSACTION, sql_engine, index=True)

        with sql_engine.connect() as conn:
            stmt = text(f'alter table {AppTables.ACCOUNT} rename column "index" to id')
            result = conn.execute(stmt)

            stmt = text(f'alter table {AppTables.TRANSACTION} rename column "index" to id')
            result = conn.execute(stmt)

    @classmethod
    @log_function_call
    def _load_csv_data(cls,
                       acc_file: str = ACCOUNTS_FILE,
                       trans_file: str = TRANSACTIONS_FILE) -> tuple[pd.DataFrame, pd.DataFrame]:
        accounts = cls._read_file(acc_file)
        transactions = cls._read_file(trans_file)

        trans_date_col = TransactionModelColumns.DATE
        amount_col = TransactionModelColumns.AMOUNT

        transactions[trans_date_col] = pd.to_datetime(transactions[trans_date_col], format='%Y-%m-%d')
        transactions[amount_col] = pd.to_numeric(transactions[amount_col])

        return accounts, transactions

    @classmethod
    @log_function_call
    def _read_file(cls, data_file: str) -> pd.DataFrame:
        """
        Read data from a CSV file in chunks and concatenate into a DataFrame.

        Args:
            data_file (str): The path to the CSV file.

        Returns:
            pd.DataFrame: The concatenated DataFrame.
        """
        full_file_path = os.path.join(DATA_FOLDER, data_file)

        try:
            CHUNK_SIZE = 1000
            chunks = pd.read_csv(full_file_path, chunksize=CHUNK_SIZE, decimal=',')
            data = pd.concat(chunks)
        except (pd.errors.DataError, pd.errors.EmptyDataError, pd.errors.ParserError) as ex:
            logger.critical(f'Issue with loading data from csv file "{full_file_path}"')
            err_msg = f'Issue with loading data from csv file "{data_file}": {ex}'
            raise pd.errors.DataError(err_msg)

        return data

