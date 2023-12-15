import logging
from datetime import date, datetime, timedelta
import calendar
import src.config as cfg

logger = logging.getLogger(cfg.LOGGER_NAME)


def get_first_day_of_the_month(dt: date) -> datetime:
    """
    Get the date with the first day of the month for a given date.

    Parameters:
    - month_date (date): The input date.

    Returns:
    - datetime: The date with the first day of the month as a datetime object.
    """
    return datetime.combine(dt.replace(day=1), datetime.min.time())


def get_last_day_of_the_month(dt: date) -> datetime:
    """
    Get the date with the last day of the month for a given date.

    Parameters:
    - month_date (date): The input date.

    Returns:
    - datetime: The date with the last day of the month as a datetime object.
    """
    return datetime.combine((dt + timedelta(days=32)).replace(day=1) - timedelta(days=1), datetime.max.time())


def get_month_name(month_date: date) -> str:
    """
    Get the name of the month for a given date.

    Parameters:
    - month_date (date): The input date.

    Returns:
    - str: The name of the month.
    """
    month_number = month_date.month
    month_name = calendar.month_name[month_number]

    return month_name


def log_function_call(func):
    def wrapper(*args, **kwargs):
        # Check if the function is a method within a class
        def get_class_name(obj):
            class_name = ''
            if hasattr(obj, '__name__'):
                class_name = obj.__name__
            elif hasattr(obj, '__class__'):
                class_name = obj.__class__.__name__
                if not class_name[0].isupper():
                    class_name = ''
            return class_name

        class_name = ''
        if args:
            class_name = get_class_name(args[0])

        if class_name:
            logger.info(f'Calling {class_name}.{func.__name__} with arguments: {args[1:]} and keyword arguments: {kwargs}')
        else:
            logger.info(f'Calling {func.__name__} with arguments: {args} and keyword arguments: {kwargs}')

        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} returned: {result}")
        return result
    return wrapper
