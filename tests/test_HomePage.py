import pytest
import allure
from allure_commons.types import AttachmentType
from TestData.HomePageData import HomePageData
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass

class TestHomePage(BaseClass):

    def test_formSubmission(self, getData):

        log = self.getLogger()
        homepage = HomePage(self.driver)

        log.info("first name is " + getData["firstname"])
        homepage.getName().send_keys(getData["firstname"])
        log.info("Last name is " + getData["lastname"])
        homepage.getEmail().send_keys(getData["lastname"])
        homepage.getCheckBox().click()
        log.info("Gender is " + getData["gender"])
        self.selectOptionByText(homepage.getGender(), getData["gender"])

        homepage.submitForm().click()
        alertText = homepage.getSuccessMessage().text

        assert ("Success" in alertText)
        self.driver.refresh()
        allure.attach(self.driver.get_screenshot_as_png(), name="HomePage", attachment_type=AttachmentType.PNG)

    @pytest.fixture(params=HomePageData.getTestData("Testcase1"))
    def getData(self, request):
        return request.param

