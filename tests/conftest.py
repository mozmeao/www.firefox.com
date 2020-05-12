import os

import pytest


DEFAULT_BASE_URL = os.getenv('BASE_URL', 'http://localhost:8080')


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", dest='base_url', default=DEFAULT_BASE_URL,
                     help="Base URL against which to run the tests")


@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption("base_url")
