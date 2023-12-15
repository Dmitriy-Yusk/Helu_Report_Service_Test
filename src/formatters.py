from datetime import date
import src.utils as utils
import src.metrics as fm
from src.utils import log_function_call


class FinanceReportFormatter:
    """
    A class responsible for formatting finance report metrics into a raw data string.
    """

    REVENUES: str = 'Revenues'
    EXPENSES: str = 'Expenses'
    PROFITS: str = 'Profits'
    MARGINS: str = 'Margins'

    @classmethod
    @log_function_call
    def format(cls, metrics: fm.FinanceReportMetrics) -> str:
        """
        Format the given finance report metrics into a raw data string.

        Args:
            metrics (fm.FinanceReportMetrics): The finance report metrics.

        Returns:
            str: The formatted raw data string.
        """
        header = cls._format_header(
            metrics.first_month.month_date,
            metrics.second_month.month_date
        )

        revenues = cls._format_revenues(
            metrics.first_month.revenue,
            metrics.second_month.revenue,
            metrics.absolute_diff.revenue,
            metrics.percent_diff.revenue
        )

        expenses = cls._format_expenses(
            metrics.first_month.expenses,
            metrics.second_month.expenses,
            metrics.absolute_diff.expenses,
            metrics.percent_diff.expenses,
        )

        profits = cls._format_profits(
            metrics.first_month.profit,
            metrics.second_month.profit,
            metrics.absolute_diff.profit,
            metrics.percent_diff.profit
        )

        margins = cls._format_margins(
            metrics.first_month.margin,
            metrics.second_month.margin,
            metrics.absolute_diff.margin,
            metrics.percent_diff.margin
        )

        raw_data = header+revenues+expenses+profits+margins

        return raw_data

    @classmethod
    def _format_header(cls, first_month_date: date, second_month_date: date):
        """
        Format the header of the finance report.

        Args:
            first_month_date (date): The date of the first month.
            second_month_date (date): The date of the second month.

        Returns:
            str: The formatted header string.
        """
        first_month_name = utils.get_month_name(first_month_date)
        second_month_name = utils.get_month_name(second_month_date)

        val = (f',"{first_month_name}, {first_month_date.year}"'
               f',"{second_month_name}, {second_month_date.year}"'
               f',"{first_month_name} vs {second_month_name}, {first_month_date.year} (Abs)"'
               f',"{first_month_name} vs {second_month_name}, {first_month_date.year} (%)"\n')

        return val

    @classmethod
    def _format_revenues(cls, col1, col2, col3, col4):
        """
        Format the revenues section of the finance report.

        Args:
            col1: Value for the first month.
            col2: Value for the second month.
            col3: Value for the absolute comparison.
            col4: Value for the percentage comparison.

        Returns:
            str: The formatted revenues string.
        """
        def_val = cls._format_by_default(col1, col2, col3, col4)
        val = f'{cls.REVENUES}{def_val}'

        return val

    @classmethod
    def _format_expenses(cls, col1, col2, col3, col4):
        """
        Format the expenses section of the finance report.

        Args:
            col1: Value for the first month.
            col2: Value for the second month.
            col3: Value for the absolute comparison.
            col4: Value for the percentage comparison.

        Returns:
            str: The formatted expenses string.
        """
        def_val = cls._format_by_default(col1, col2, col3, col4)
        val = f'{cls.EXPENSES}{def_val}'

        return val

    @classmethod
    def _format_profits(cls, col1, col2, col3, col4):
        """
        Format the profits section of the finance report.

        Args:
            col1: Value for the first month.
            col2: Value for the second month.
            col3: Value for the absolute comparison.
            col4: Value for the percentage comparison.

        Returns:
            str: The formatted profits string.
        """
        def_val = cls._format_by_default(col1, col2, col3, col4)
        val = f'{cls.PROFITS}{def_val}'

        return val

    @classmethod
    def _format_margins(cls, col1, col2, col3, col4):
        """
        Format the margins section of the finance report.

        Args:
            col1: Value for the first month.
            col2: Value for the second month.
            col3: Value for the absolute comparison.
            col4: Value for the percentage comparison.

        Returns:
            str: The formatted margins string.
        """
        val = (f'{cls.MARGINS}'
               f',{col1:.1f}%'
               f',{col2:.1f}%'
               f',{col3:.1f} p.p.'
               f',{col4:.1f}%\n')

        return val

    @classmethod
    def _format_by_default(cls, col1, col2, col3, col4):
        """
        Format values by default for finance report columns.
        It is the common pattern for Revenues, Expenses and Profits

        Args:
            col1: Value for the first month.
            col2: Value for the second month.
            col3: Value for the absolute comparison.
            col4: Value for the percentage comparison.

        Returns:
            str: The formatted values by default string.
        """
        val = (f',{col1:.2f}'
               f',{col2:.2f}'
               f',{col3:.2f}'
               f',{col4:.1f}%\n')

        return val
