import logging
from typing import List
from datetime import date
from abc import ABC, abstractmethod
from sqlalchemy import text

import src.utils as utils
from src.models import TransactionWithAccount, Transaction, AppTables, TransactionType, AccountNature
from src.data_adapters import SQLEngine
from src.metrics import BaseFinanceMetrics
from src.utils import log_function_call


class MonthDataBaseDataSource(ABC):
    @classmethod
    @abstractmethod
    def get(cls, date_info: date):
        pass


class TransactionsMonthData(MonthDataBaseDataSource):
    @classmethod
    @log_function_call
    def get(cls, date_info: date) -> List[TransactionWithAccount]:
        date_start = utils.get_first_day_of_the_month(date_info)
        date_end = utils.get_last_day_of_the_month(date_info)

        session = SQLEngine.get_session()

        with session:
            result = (session.query(TransactionWithAccount)
                      .filter(Transaction.transaction_date >= date_start,
                              Transaction.transaction_date <= date_end))

            month_transactions = [row for row in result]

        return month_transactions


class MetricsMonthData(MonthDataBaseDataSource):
    @classmethod
    @log_function_call
    def get(cls, date_info: date) -> BaseFinanceMetrics:
        date_start = utils.get_first_day_of_the_month(date_info)
        date_end = utils.get_last_day_of_the_month(date_info)

        values = {
            'income':     AccountNature.INCOME,
            'expense':    AccountNature.EXPENSE,
            'credit':     TransactionType.CREDIT,
            'debit':      TransactionType.DEBIT,
            'date_start': date_start,
            'date_end':   date_end,
        }

        engine = SQLEngine.get()

        with engine.connect() as conn:
            stmt = text(f'select '
                            f'basic_metrics.revenues,	'
                            f'basic_metrics.expenses,	'
                            f'(basic_metrics.revenues + basic_metrics.expenses) as profits, '
                            f'iif(basic_metrics.revenues != 0, '
                                f'(basic_metrics.revenues + basic_metrics.expenses) * 100/basic_metrics.revenues, '
                                f'0) as margins '
                        f'from ('
                            f'select '
                                f'sum(iif(month_trans.account_nature == :income and month_trans.transaction_type == :credit, '
                                    f'month_trans.amount, '
                                    f'iif(month_trans.account_nature == :income and month_trans.transaction_type == :debit, '
                                        f'-month_trans.amount, 0))) as revenues, '
                                f'sum(iif(month_trans.account_nature == :expense and month_trans.transaction_type == :credit, '
                                    f'month_trans.amount, '
                                    f'iif(month_trans.account_nature == :expense and month_trans.transaction_type == :debit, '
                                        f'-month_trans.amount, 0))) as expenses '
                            f'from ('
                                f'select ts.*, ac.account_nature '
                                f'from {AppTables.TRANSACTION} ts, {AppTables.ACCOUNT} ac '
                                f'where '
                                    f'ts.account_code = ac.account_code '
                                    f'and ts.transaction_date >= :date_start '
                                    f'and ts.transaction_date <= :date_end'
                            f') month_trans'
                        f') basic_metrics')

            row = conn.execute(stmt, values).first()

            metrics = BaseFinanceMetrics()
            metrics.revenue = row[0]
            metrics.expenses = row[1]
            metrics.profit = row[2]
            metrics.margin = row[3]

        return metrics

