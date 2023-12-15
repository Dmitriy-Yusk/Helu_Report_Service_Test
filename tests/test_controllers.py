import src.models as models
from src.metrics import FinanceMetricsExtCalculator


def test__get_revenue_in_row():
    acc_nature = models.AccountNature.INCOME
    trans_type = models.TransactionType.CREDIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._get_revenue_in_row(acc_nature, trans_type, amount)
    eq = new_amount == amount
    assert eq

    acc_nature = models.AccountNature.INCOME
    trans_type = models.TransactionType.DEBIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._get_revenue_in_row(acc_nature, trans_type, amount)
    eq = new_amount == -amount
    assert eq

    acc_nature = models.AccountNature.EXPENSE
    trans_type = models.TransactionType.DEBIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._get_revenue_in_row(acc_nature, trans_type, amount)
    eq = new_amount == 0
    assert eq

    acc_nature = models.AccountNature.EXPENSE
    trans_type = models.TransactionType.CREDIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._get_revenue_in_row(acc_nature, trans_type, amount)
    eq = new_amount == 0
    assert eq


def test__get_expense_in_row():
    acc_nature = models.AccountNature.EXPENSE
    trans_type = models.TransactionType.CREDIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._get_expense_in_row(acc_nature, trans_type, amount)
    eq = new_amount == amount
    assert eq

    acc_nature = models.AccountNature.EXPENSE
    trans_type = models.TransactionType.DEBIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._get_expense_in_row(acc_nature, trans_type, amount)
    eq = new_amount == -amount
    assert eq

    acc_nature = models.AccountNature.INCOME
    trans_type = models.TransactionType.CREDIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._get_expense_in_row(acc_nature, trans_type, amount)
    eq = new_amount == 0
    assert eq

    acc_nature = models.AccountNature.INCOME
    trans_type = models.TransactionType.DEBIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._get_expense_in_row(acc_nature, trans_type, amount)
    eq = new_amount == 0
    assert eq


def test__calc_amount():
    trans_type = models.TransactionType.CREDIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._calc_amount(trans_type, amount)
    eq = amount == new_amount
    assert eq

    trans_type = models.TransactionType.DEBIT
    amount = 1
    new_amount = FinanceMetricsExtCalculator._calc_amount(trans_type, amount)
    eq = amount == -new_amount
    assert eq

    trans_type = 'garbage'
    amount = 1
    new_amount = FinanceMetricsExtCalculator._calc_amount(trans_type, amount)
    eq = new_amount == 0
    assert eq
