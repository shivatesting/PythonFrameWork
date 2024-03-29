import os
import shutil
import configparser
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager

driver = None


@pytest.fixture(scope="class")
def setup(request):
    global driver
    current_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_directory, 'config.properties')
    config = configparser.ConfigParser()
    config.read(config_file_path)

    browser_name = config['AllDetails']['browser_name']
    url = config['AllDetails']['url']

    if browser_name == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == "IE":
        driver = webdriver.Ie(IEDriverManager().install())
    elif browser_name == "Edge":
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

    driver.maximize_window()

    driver.get(url)
    request.cls.driver = driver
    yield
    driver.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def log_on_failure(request):
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="failed_test", attachment_type=AttachmentType.PNG)
    else:
        allure.attach(driver.get_screenshot_as_png(), name="passed_test", attachment_type=AttachmentType.PNG)


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)


@pytest.fixture(scope='session', autouse=True)
def cleanup_files_before_test(request):
    folder_path = 'C:/Users/shiva.chaudhary/PycharmProjects/PythonSelfFramework/pythonProject/allure-results'

    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    # os.mkdir('screenshot')
            except Exception as e:
                print(f"Error while deleting {file_path}: {e}")
