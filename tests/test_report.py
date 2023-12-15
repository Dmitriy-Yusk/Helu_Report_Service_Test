from datetime import date
from starlette.testclient import TestClient


def test_report(client: TestClient, file_regression):
    """
    Given a GET request to an endpoint /report,
    The response should match with provided test_report.csv file
    """

    first_date_default = date(year=2020, month=6, day=15)
    second_date_default = date(year=2020, month=5, day=15)

    response = client.get(f'/report?first_date={first_date_default.isoformat()}&second_date={second_date_default.isoformat()}')

    file_regression.check(response.content, extension=".csv", binary=True)
