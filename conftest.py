import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def pytest_addoption(parser):
    """
    Add test run flags to the invocation parameters to allow setting of selenium explicit waits for slow sites
    and option to use selenium grid for CI/CD integration
    """
    parser.addoption("--global_wait_time_out",default="100", help="Maximum time to implicitly wait for page load (pools every 500ms)")
    parser.addoption("--remote",  action="store_true" , help="determine if to run in remote mode using selenium grid docker containers")

@pytest.fixture(scope='session')
def remote(request):
    return request.config.getoption("--remote")

@pytest.fixture(scope='session')
def global_wait_time_out(request):
    return request.config.getoption("--global_wait_time_out")

@pytest.fixture
def driver(remote):
    """
    Set up and tear down the WebDriver for the test.
    """
    if remote:
        remote_selenium_fqdn = os.environ.get("SELENIUM_HOST", "http://selenium-hub:4444/wd/hub")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--enable-gpu")
        driver = webdriver.Remote(remote_selenium_fqdn, options=options)
    else:
        driver = webdriver.Chrome() # use default options
    yield driver
    driver.quit()