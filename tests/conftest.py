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
import os

driver = None
current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'config.properties')
config = configparser.ConfigParser()
config.read(config_file_path)

@pytest.fixture(scope="class")
def setup(request):
    global driver  # Global variable to hold the WebDriver instance

    # Retrieve browser name and URL from configuration
    browser_name = config['AllDetails']['browser_name']
    url = config['AllDetails']['url']

    # Initialize WebDriver based on the browser specified in the configuration
    if browser_name == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == "IE":
        driver = webdriver.Ie(IEDriverManager().install())
    elif browser_name == "Edge":
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

    # Maximize the window to ensure consistent testing environment
    driver.maximize_window()

    # Open the specified URL
    driver.get(url)

    # Set the WebDriver instance to the class attribute for test classes to access
    request.cls.driver = driver

    # This acts as a teardown method, cleaning up resources used during testing
    yield

    # Close the browser window after the test execution is complete
    driver.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    # Access the pytest_html plugin for generating HTML reports
    pytest_html = item.config.pluginmanager.getplugin('html')
    # Allow the hook to continue its execution
    outcome = yield
    # Retrieve the test report
    report = outcome.get_result()
    # Get the 'extra' attribute from the report or initialize an empty list if it doesn't exist
    extra = getattr(report, 'extra', [])

    # Check if the report is generated during test execution (call) or setup
    if report.when == 'call' or report.when == "setup":
        # Check if the test was expected to fail
        xfail = hasattr(report, 'wasxfail')
        # Check if the test was skipped and expected to fail or if the test failed and was not expected to fail
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Generate a file name based on the test node ID
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)  # Capture a screenshot and save it with the generated file name

            # If the file name exists, create HTML to embed the screenshot in the report
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))  # Append the HTML to the 'extra' attribute
        # Update the 'extra' attribute in the report
        report.extra = extra


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def log_on_failure(request):
    # The fixture yields, allowing the test function to execute
    yield
    # Retrieve the test item (node) from the request
    item = request.node
    # Check if the test call (execution) failed
    if item.rep_call.failed:
        # If the test failed, attach a screenshot to the Allure report
        allure.attach(driver.get_screenshot_as_png(), name="failed_test", attachment_type=AttachmentType.PNG)
    else:
        # If the test passed, attach a screenshot to the Allure report with a different name
        allure.attach(driver.get_screenshot_as_png(), name="passed_test", attachment_type=AttachmentType.PNG)


def _capture_screenshot(name, driver, folder="screenshots"):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        screenshot_path = os.path.join(folder, name)
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")

@pytest.fixture(scope="session", autouse=True)
def clean_screenshot_folder_before_suite():
    """Fixture to clean the screenshot folder before starting a test suite."""
    folder = config['AllDetails']['folder']
    try:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    except Exception as e:
        print(f"Failed to clean screenshot folder: {e}")

@pytest.fixture(scope='function', autouse=True)
def screenshot_after_each_step(request):
    yield
    item = request.node
    if item.rep_call.failed:
        # If the test failed, no need to capture another screenshot
        return
    step_number = 1
    for step in item.iter_markers(name='step'):
        step_name = step.kwargs.get('name', f'Step {step_number}')
        file_name = f"{item.nodeid}_{step_name}.png"
        _capture_screenshot(file_name)
        step_number += 1


@pytest.fixture(scope='session', autouse=True)
def cleanup_files_before_test(request):
    # Retrieve the folder path from the configuration
    folder_path = config['AllDetails']['folder_path']

    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate over each file in the folder
        for file_name in os.listdir(folder_path):
            # Construct the full path to the file
            file_path = os.path.join(folder_path, file_name)
            try:
                # Check if the file is a regular file (not a directory
                if os.path.isfile(file_path):
                    # If it's a file, delete it
                    os.unlink(file_path)
                # If it's a directory, delete it recursively
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            except Exception as e:
                # If an error occurs during deletion, print the error message
                print(f"Error while deleting {file_path}: {e}")
