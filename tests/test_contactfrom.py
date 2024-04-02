import pytest
from TestData.HomePageData import HomePageData
from pageObjects.HomePage import HomePage
from tests.conftest import _capture_screenshot
from utilities.BaseClass import BaseClass


@pytest.mark.smoke
@pytest.mark.priority_medium
class TestHomePage(BaseClass):

    def test_formSubmission(self, getData, screenshot_after_each_step):
        log = self.getLogger()  # Retrieve logger for logging purposes
        homepage = HomePage(self.driver)  # Initialize the HomePage object

        # Step 1: Enter first name
        log.info("first name is " + getData["firstname"])  # Log information about the first name
        homepage.getName().send_keys(getData["firstname"])  # Enter first name in the form
        _capture_screenshot("step1_homepage_screenshot.png", self.driver)  # Capture a screenshot after step 1

        # Step 2: Enter email
        log.info("Email is " + getData["Email"])  # Log information about the email
        homepage.getEmail().send_keys(getData["Email"])  # Enter email in the form
        _capture_screenshot("step2_homepage_screenshot.png", self.driver)  # Capture a screenshot after step 2

        # Step 3: Check the checkbox
        homepage.getCheckBox().click()  # Check the checkbox
        _capture_screenshot("step3_homepage_screenshot.png", self.driver)  # Capture a screenshot after step 3

        # Step 4: Select gender from the dropdown
        log.info("Gender is " + getData["gender"])  # Log information about the gender
        self.selectOptionByText(homepage.getGender(), getData["gender"])  # Select gender from the dropdown
        _capture_screenshot("step4_homepage_screenshot.png", self.driver)  # Capture a screenshot after step 4

        # Step 5: Submit the form
        homepage.submitForm().click()  # Submit the form
        alertText = homepage.getSuccessMessage().text  # Get the success message from the alert
        _capture_screenshot("step5_homepage_screenshot.png", self.driver)  # Capture a screenshot after step 5

        # Step 6: Verify success message
        assert ("Success" in alertText)  # Assert if the success message contains "Success"
        self.driver.refresh()  # Refresh the page for the next test
        _capture_screenshot("step6_homepage_screenshot.png", self.driver)  # Capture a screenshot after step 6

    # Fixture to parameterize test data
    @pytest.fixture(params=HomePageData.getTestData("Testcase1"))
    def getData(self, request):
        return request.param
