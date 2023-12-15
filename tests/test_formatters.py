from datetime import date
from src.formatters import FinanceReportFormatter


def test_finance_report_stream_header_formatter():
    first_month_date = date(year=2020, month=6, day=2)
    second_month_date = date(year=2020, month=5, day=3)

    value = FinanceReportFormatter._format_header(first_month_date, second_month_date)
    example_value = ',"June, 2020","May, 2020","June vs May, 2020 (Abs)","June vs May, 2020 (%)"\n'

    eq = value == example_value
    assert eq


def test_finance_report_stream_default_formatter():
    col1 = -1.11
    col2 = -2.22
    col3 = -3.33
    col4 = -4.4

    value = FinanceReportFormatter._format_by_default(col1, col2, col3, col4)
    example_value = ',-1.11,-2.22,-3.33,-4.4%\n'

    eq = value == example_value
    assert eq


def test_finance_report_stream_revenue_formatter():
    col1 = 1.11
    col2 = 2.22
    col3 = 3.33
    col4 = 4.4

    value = FinanceReportFormatter._format_revenues(col1, col2, col3, col4)
    example_value = f'{FinanceReportFormatter.REVENUES},1.11,2.22,3.33,4.4%\n'

    eq = value == example_value
    assert eq


def test_finance_report_stream_expenses_formatter():
    col1 = 1.11
    col2 = 2.22
    col3 = 3.33
    col4 = 4.4

    value = FinanceReportFormatter._format_expenses(col1, col2, col3, col4)
    example_value = f'{FinanceReportFormatter.EXPENSES},1.11,2.22,3.33,4.4%\n'

    eq = value == example_value
    assert eq


def test_finance_report_stream_profits_formatter():
    col1 = 1.11
    col2 = 2.22
    col3 = 3.33
    col4 = 4.4

    value = FinanceReportFormatter._format_profits(col1, col2, col3, col4)
    example_value = f'{FinanceReportFormatter.PROFITS},1.11,2.22,3.33,4.4%\n'

    eq = value == example_value
    assert eq


def test_finance_report_stream_margins_formatter():
    col1 = -1.11
    col2 = -2.22
    col3 = -3.33
    col4 = -4.4

    value = FinanceReportFormatter._format_margins(col1, col2, col3, col4)
    example_value = f'{FinanceReportFormatter.MARGINS},-1.1%,-2.2%,-3.3 p.p.,-4.4%\n'

    eq = value == example_value
    assert eq
