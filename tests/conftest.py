import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

import logging
import src.config as cfg
from src.main import app as orig_app


@pytest.fixture
def app() -> FastAPI:
    testing_app = orig_app

    return testing_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def pytest_configure(config):
    log_lvl = 'ERROR'

    app_logger = logging.getLogger(cfg.LOGGER_NAME)
    app_logger.setLevel(log_lvl)

    root_logger = logging.getLogger('root')
    root_logger.setLevel(log_lvl)
