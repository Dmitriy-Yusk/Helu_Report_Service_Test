from datetime import date
from typing import List
from abc import ABC, abstractmethod

from src.utils import log_function_call
import src.models as models
import src.metrics as fm
import src.data_helpers as dh


class FinanceReportServiceController:
    def __init__(self, data_source_class: dh.MonthDataBaseDataSource, metrics_calculator_calc: fm.BaseMetricsCalculator):
        """
        Initializes the FinanceReportServiceController.

        Parameters:
        - first_date (date): The start date for the first month.
        - second_date (date): The start date for the second month.
        """
        self.__calculator_class = metrics_calculator_calc
        self.__data_source = data_source_class

    @log_function_call
    def calculate_metrics(self, first_date: date, second_date: date) -> fm.FinanceReportMetrics:
        """
        Calculates finance metrics.

        Returns:
        - fm.FinanceReportMetrics: The calculated finance metrics.
        """
        metrics: fm.FinanceReportMetrics = fm.FinanceReportMetricsBuilder.create_object(
            first_date,
            second_date
        )

        first_month_trans = self.__data_source.get(first_date)
        second_month_trans = self.__data_source.get(second_date)

        self.__calculator_class.execute(
            first_month_trans,
            second_month_trans,
            metrics
        )

        return metrics
