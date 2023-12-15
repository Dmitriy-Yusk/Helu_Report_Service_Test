from dataclasses import dataclass
from datetime import date, datetime
from typing import List
from abc import ABC, abstractmethod

import src.models as models
from src.utils import log_function_call


@dataclass
class BaseFinanceMetrics:
    """Base class for financial metrics."""
    revenue: float = 0
    expenses: float = 0
    profit: float = 0
    margin: float = 0

    def copy_to(self, copy_to_obj):
        copy_to_obj.revenue = self.revenue
        copy_to_obj.expenses = self.expenses
        copy_to_obj.profit = self.profit
        copy_to_obj.margin = self.margin


@dataclass
class MonthFinanceMetrics(BaseFinanceMetrics):
    """Class for financial metrics for a specific month."""
    month_date: date = None

    def __init__(self, month_date: date):
        self.month_date = month_date


@dataclass
class MonthsDifferenceFinanceMetrics(BaseFinanceMetrics):
    """Class for the difference between two MonthFinanceMetrics instances."""
    first_month: MonthFinanceMetrics = None
    second_month: MonthFinanceMetrics = None

    def __init__(self, first_month: MonthFinanceMetrics, second_month: MonthFinanceMetrics):
        self.first_month = first_month
        self.second_month = second_month


@dataclass
class FinanceReportMetrics:
    """Class for summarizing financial metrics for a report."""
    first_month: MonthFinanceMetrics = None
    second_month: MonthFinanceMetrics = None
    absolute_diff: MonthsDifferenceFinanceMetrics = None
    percent_diff: MonthsDifferenceFinanceMetrics = None


class FinanceReportMetricsBuilder:
    @classmethod
    @log_function_call
    def create_object(cls, first_date: date, second_date: date) -> FinanceReportMetrics:
        """
        FinanceMetrics builder function - Create FinanceReportMetrics instance.

        Parameters:
        - first_date (date): The date for the first month.
        - second_date (date): The date for the second month.

        Returns:
        FinanceReportMetrics: The initialized FinanceReportMetrics instance.
        """
        metrics = FinanceReportMetrics()

        first_month = MonthFinanceMetrics(first_date)
        second_month = MonthFinanceMetrics(second_date)

        metrics.first_month = first_month
        metrics.second_month = second_month

        metrics.absolute_diff = MonthsDifferenceFinanceMetrics(first_month, second_month)
        metrics.percent_diff = MonthsDifferenceFinanceMetrics(first_month, second_month)

        return metrics


class BaseMetricsCalculator(ABC):
    @classmethod
    @log_function_call
    def execute(cls, first_month_data, second_month_data, metrics: FinanceReportMetrics) -> None:
        """
        Executes the calculation of finance metrics.

        Parameters:
        - first_month_data (List[models.TransactionAggregationModel]): Data for the first month.
        - second_month_data (List[models.TransactionAggregationModel]): Data for the second month.
        - metrics (fm.FinanceReportMetrics): Object to store calculated finance metrics.

        Returns:
        - None
        """
        cls._calc_month_metrics(first_month_data, metrics.first_month)
        cls._calc_month_metrics(second_month_data, metrics.second_month)

        cls._calc_month_diff_absolute_metrics(metrics.absolute_diff)
        cls._calc_month_diff_percentage_metrics(metrics.percent_diff)

    @classmethod
    @abstractmethod
    def _calc_month_metrics(cls, data, metrics: BaseFinanceMetrics) -> None:
        pass

    @classmethod
    def _calc_month_diff_absolute_metrics(cls, metrics: MonthsDifferenceFinanceMetrics) -> None:
        """
        Calculates absolute differences in finance metrics between two months.

        Parameters:
        - metrics (fm.MonthsDifferenceFinanceMetrics): Object to store calculated absolute differences.

        Returns:
        - None
        """
        metrics.revenue = metrics.first_month.revenue - metrics.second_month.revenue
        metrics.expenses = metrics.first_month.expenses - metrics.second_month.expenses
        metrics.profit = metrics.first_month.profit - metrics.second_month.profit
        metrics.margin = metrics.first_month.margin - metrics.second_month.margin

    @classmethod
    def _calc_month_diff_percentage_metrics(cls, metrics: MonthsDifferenceFinanceMetrics) -> None:
        """
        Calculates percentage differences in finance metrics between two months.

        Parameters:
        - metrics (fm.MonthsDifferenceFinanceMetrics): Object to store calculated percentage differences.

        Returns:
        - None
        """
        if metrics.second_month.revenue != 0:
            metrics.revenue = (metrics.first_month.revenue - metrics.second_month.revenue)*100/abs(metrics.second_month.revenue)
        if metrics.second_month.expenses != 0:
            metrics.expenses = (metrics.first_month.expenses - metrics.second_month.expenses)*100/abs(metrics.second_month.expenses)
        if metrics.second_month.profit != 0:
            metrics.profit = (metrics.first_month.profit - metrics.second_month.profit)*100/abs(metrics.second_month.profit)
        if metrics.second_month.margin != 0:
            metrics.margin = (metrics.first_month.margin - metrics.second_month.margin)*100/abs(metrics.second_month.margin)


class FinanceMetricsSimpleCalculator(BaseMetricsCalculator):
    @classmethod
    def _calc_month_metrics(cls, data: BaseFinanceMetrics, metrics: BaseFinanceMetrics) -> None:
        data.copy_to(metrics)


class FinanceMetricsExtCalculator(BaseMetricsCalculator):
    @classmethod
    def _calc_month_metrics(cls, data: List[models.TransactionWithAccount], metrics: BaseFinanceMetrics) -> None:
        """
        Calculates month-specific finance metrics.

        Parameters:
        - data (List[models.TransactionAggregationModel]): List of transactions for the month.
        - metrics (fm.BaseFinanceMetrics): Object to store calculated finance metrics.

        Returns:
        - None
        """
        for transaction in data:
            metrics.revenue += cls._get_revenue_in_row(
                transaction.account_nature,
                transaction.transaction_type,
                transaction.amount
            )

            metrics.expenses += cls._get_expense_in_row(
                transaction.account_nature,
                transaction.transaction_type,
                transaction.amount
            )

        metrics.profit = cls._calc_profit(metrics)
        metrics.margin = cls._calc_margin(metrics)

    @staticmethod
    def _get_revenue_in_row(acc_nature: str, trans_type: str, amount: float) -> float:
        """
        Calculates revenue for a given transaction.

        Parameters:
        - acc_nature (str): Account nature of the transaction.
        - trans_type (str): Transaction type (credit/debit).
        - amount (float): Transaction amount.

        Returns:
        - float: Calculated revenue.
        """
        # Revenues = (income credit) - (income debit)
        new_amount: float = 0

        if acc_nature != models.AccountNature.INCOME:
            return new_amount

        new_amount = FinanceMetricsExtCalculator._calc_amount(trans_type, amount)

        return new_amount

    @staticmethod
    def _get_expense_in_row(acc_nature: str, trans_type: str, amount: float) -> float:
        """
        Calculates expenses for a given transaction.

        Parameters:
        - acc_nature (str): Account nature of the transaction.
        - trans_type (str): Transaction type (credit/debit).
        - amount (float): Transaction amount.

        Returns:
        - float: Calculated expenses.
        """
        # Expenses = (expenses credit) - (expenses debit)
        new_amount: float = 0

        if acc_nature != models.AccountNature.EXPENSE:
            return new_amount

        new_amount = FinanceMetricsExtCalculator._calc_amount(trans_type, amount)

        return new_amount

    @staticmethod
    def _calc_amount(trans_type: str, amount: float) -> float:
        """
        Calculates the amount based on the transaction type.

        Parameters:
        - trans_type (str): Transaction type (credit/debit).
        - amount (float): Transaction amount.

        Returns:
        - float: Calculated amount.
        """
        ret_amount: float = 0

        if trans_type == models.TransactionType.CREDIT:
            ret_amount = amount
        elif trans_type == models.TransactionType.DEBIT:
            ret_amount = -amount

        return ret_amount

    @staticmethod
    def _calc_profit(metrics: BaseFinanceMetrics) -> float:
        """
        Calculates profits based on revenues and expenses.

        Parameters:
        - metrics (fm.BaseFinanceMetrics): Object containing finance metrics.

        Returns:
        - float: Calculated profits.
        """
        # Profits = Revenues + Expenses
        return metrics.revenue + metrics.expenses

    @staticmethod
    def _calc_margin(metrics: BaseFinanceMetrics) -> float:
        """
        Calculates margins based on profits and revenues.

        Parameters:
        - metrics (fm.BaseFinanceMetrics): Object containing finance metrics.

        Returns:
        - float: Calculated profit margin.
        """
        # Margin = Profits / Revenues * 100
        margin = 0
        if metrics.revenue != 0:
            margin = metrics.profit / metrics.revenue * 100
        return margin
