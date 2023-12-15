import logging
from datetime import date

import src.data_adapters as da
import src.data_helpers as dh
import src.metrics as m


def test_get_month_data():
    eq = False

    try:
        da.DataLoader.load(engine=da.SQLEngine, acc_file=da.ACCOUNTS_FILE, trans_file=da.TRANSACTIONS_FILE)

        dt = date(year=2020, month=6, day=15)

        transactions = dh.TransactionsMonthData.get(dt)

        eq = len(transactions) == 111
    except Exception as ex:
        logging.critical(msg='', exc_info=ex)
        raise ex
    finally:
        da.SQLEngine.clear()

    assert eq


def test_get_month_metrics():
    eq = False

    def compare_metrics(m1: m.BaseFinanceMetrics, m2: m.BaseFinanceMetrics) -> bool:
        return (int(m1.revenue) == int(m2.revenue) and
                int(m1.expenses) == int(m2.expenses) and
                int(m1.profit) == int(m2.profit) and
                int(m1.margin) == int(m2.margin))

    try:
        da.DataLoader.load(engine=da.SQLEngine, acc_file=da.ACCOUNTS_FILE, trans_file=da.TRANSACTIONS_FILE)

        dt = date(year=2020, month=6, day=15)

        metrics = dh.MetricsMonthData.get(dt)

        etalon = m.BaseFinanceMetrics()
        etalon.revenue = 13393.15
        etalon.expenses = -34633.91
        etalon.profit = -21240.76
        etalon.margin = -158.6

        eq = compare_metrics(metrics, etalon)

    except Exception as ex:
        logging.critical(msg='', exc_info=ex)
        raise ex
    finally:
        da.SQLEngine.clear()

    assert compare_metrics(metrics, etalon)
