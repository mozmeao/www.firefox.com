import pytest


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", dest='base_url', default='http://localhost:8080',
                     help="Base URL against which to run the tests")


@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption("base_url")
