import pytest
from TestData.HomePageData import HomePageData
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class TestHomePage(BaseClass):

    def test_formSubmission(self, getData):
        log = self.getLogger()  # Retrieve logger for logging purposes
        homepage = HomePage(self.driver)  # Initialize the HomePage object

        log.info("first name is " + getData["firstname"])  # Log information about the first name
        homepage.getName().send_keys(getData["firstname"])  # Enter first name in the form
        log.info("Email is " + getData["Email"])  # Log information about the email
        homepage.getEmail().send_keys(getData["Email"])  # Enter email in the form
        homepage.getCheckBox().click()  # Check the checkbox
        log.info("Gender is " + getData["gender"])  # Log information about the gender
        self.selectOptionByText(homepage.getGender(), getData["gender"])  # Select gender from the dropdown

        homepage.submitForm().click()  # Submit the form
        alertText = homepage.getSuccessMessage().text  # Get the success message from the alert

        assert ("Success" in alertText)  # Assert if the success message contains "Success"
        self.driver.refresh()  # Refresh the page for the next test

    # Fixture to parameterize test data
    @pytest.fixture(params=HomePageData.getTestData("Testcase1"))
    def getData(self, request):
        return request.param
