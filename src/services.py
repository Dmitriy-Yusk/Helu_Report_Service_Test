from src.utils import log_function_call
from src.controllers import FinanceReportServiceController
from src.formatters import FinanceReportFormatter
from src.metrics import FinanceReportMetrics, FinanceMetricsExtCalculator, FinanceMetricsSimpleCalculator
from src.data_adapters import DataLoader, SQLEngine, ACCOUNTS_FILE, TRANSACTIONS_FILE
from src.data_helpers import TransactionsMonthData, MetricsMonthData
from datetime import date


@log_function_call
def generate_finance_report(first_date: date, second_date: date) -> str:
    """
    Generate a finance report based on the specified date range.

    Parameters:
    - first_date (date): The first month of the report.
    - second_date (date): The second month of the report.

    Returns:
    str: A formatted finance report as a string.
    """

    DataLoader.load(engine=SQLEngine, acc_file=ACCOUNTS_FILE, trans_file=TRANSACTIONS_FILE)

    # report_controller = FinanceReportServiceController(
    #     data_source_class=TransactionsMonthData,
    #     metrics_calculator_calc=FinanceMetricsExtCalculator
    # )
    report_controller = FinanceReportServiceController(
        data_source_class=MetricsMonthData,
        metrics_calculator_calc=FinanceMetricsSimpleCalculator
    )

    report_metrics = report_controller.calculate_metrics(first_date, second_date)

    raw_data = FinanceReportFormatter.format(report_metrics)

    return raw_data
