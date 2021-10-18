import calendar
import time
import pytest

def pytest_addoption(parser):
    parser.addoption("--baseUrl", action="store", default="http://127.0.0.1:5000/",help="baseUrl")



@pytest.fixture()
def get_base_url(pytestconfig):
    return pytestconfig.option.baseUrl          


@pytest.fixture()
def BASEURL(get_base_url):
    return get_base_url  

@pytest.fixture()
def UNIQ_USER():
    """Return username and password by template : user_{timestamp}"""
    unique=calendar.timegm(time.gmtime())
    return  {
              "username":f"user_{unique}", 
              "password":f"password_{unique}"
              }              