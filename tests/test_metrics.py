from dataclasses import dataclass
from datetime import date, datetime
from typing import List
from abc import ABC, abstractmethod

import src.models as models
import src.metrics as metrics


def test_metrics_obj_copy():
    metrics1 = metrics.BaseFinanceMetrics()
    metrics1.revenue = 1
    metrics1.expenses = 2
    metrics1.profit = 3
    metrics1.margin = 4

    metrics2 = metrics.BaseFinanceMetrics()

    metrics1.copy_to(metrics2)

    def compare(m1: metrics.BaseFinanceMetrics, m2: metrics.BaseFinanceMetrics) -> bool:
        return (m1.revenue == m2.revenue and
                m1.expenses == m2.expenses and
                m1.profit == m2.profit and
                m1.margin == m2.margin)

    assert compare(metrics1, metrics2)
