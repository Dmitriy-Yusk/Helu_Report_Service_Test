import inspect
from datetime import date
import logging

import pandas as pd
from sqlite3 import Error as SQLiteError
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response

import src.config as cfg
import src.services as services


cfg.init_logging()
logger = logging.getLogger(cfg.LOGGER_NAME)

app = FastAPI()


@app.get("/")
def hello_handler():
    return {"msg": "Hello, World!"}


@app.get("/report")
def get_report(
    first_date: date,
    second_date: date,
):
    err_msg = ''
    err_status_code = 500

    report_data = ''

    try:
        report_data = services.generate_finance_report(first_date, second_date)
    except (SQLiteError, SQLAlchemyError) as ex:
        err_msg = 'Issue with SQL database'
        logger.critical(f'{ex}')
    except pd.errors.DataError as ex:
        err_msg = f'{ex}'
    except (pd.errors.EmptyDataError, pd.errors.MergeError, pd.errors.ParserError) as ex:
        err_msg = f'Issue with loading data from csv files: {ex}'
    except ValueError as ex:
        err_msg = f'{ex}'

    if err_msg != '':
        logger.critical(err_msg)
        raise HTTPException(status_code=err_status_code, detail=err_msg)

    return Response(report_data)
