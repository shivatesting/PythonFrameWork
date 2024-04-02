import os
import configparser

import pytest

from pageObjects.HomePage import HomePage
from tests.conftest import _capture_screenshot
from utilities.BaseClass import BaseClass


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.priority_high
class TestOne(BaseClass):

    def test_e2e(self, screenshot_after_each_step):
        log = self.getLogger()  # Retrieve logger for logging purposes

        # Initialize the pages needed for the test
        homePage = HomePage(self.driver)

        checkoutPage = homePage.shopItems()

        # Load configuration from config.properties
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_directory, 'config.properties')
        config = configparser.ConfigParser()
        config.read(config_file_path)

        country_name = config['AllDetails']['country_name']
        product_title = config['AllDetails']['product_title']
        country_name_verify = config['AllDetails']['country_name_verify']

        # Log information about the operation
        log.info("getting all the card titles")

        # Get all card titles from the checkout page
        cards = checkoutPage.getCardTitles()
        i = -1
        # Iterate through each card
        for card in cards:
            i = i + 1
            cardText = card.text
            log.info(cardText)
            # If the card title is "Blackberry", click on its corresponding footer
            if cardText == product_title:
                checkoutPage.getCardFooter()[i].click()

        _capture_screenshot("step1_orderofproducts_screenshot.png", self.driver)  # Capture a screenshot after step 1

        checkoutPage = homePage.checkoutNavs()  # Navigate to the checkout page
        _capture_screenshot("step2_orderofproducts_screenshot.png", self.driver)  # Capture a screenshot after step 2

        confirmPage = checkoutPage.checkOutItems()  # Proceed with checking out items

        # Log information about the operation
        log.info("Entering country name as " + country_name)

        # Enter the country name ind
        confirmPage.getCountyName().send_keys(country_name)
        _capture_screenshot("step3_orderofproducts_screenshot.png", self.driver)  # Capture a screenshot after step 3

        self.verifyLinkPresence(country_name_verify)  # Verify if "India" appears in the dropdown
        _capture_screenshot("step4_orderofproducts_screenshot.png", self.driver)  # Capture a screenshot after step 4

        confirmPage.getcountyNameList().click()  # Select the country from the dropdown
        _capture_screenshot("step5_orderofproducts_screenshot.png", self.driver)  # Capture a screenshot after step 5

        log.info("Selected country name")  # Log information about the operation
        confirmPage.getAgreeCheckbox().click()  # Agree to the terms by clicking the checkbox
        _capture_screenshot("step6_orderofproducts_screenshot.png", self.driver)  # Capture a screenshot after step 6

        confirmPage.getPurchaseButton().click()  # Proceed with the purchase by clicking the purchase button
        _capture_screenshot("step7_orderofproducts_screenshot.png", self.driver)  # Capture a screenshot after step 7

        textMatch = confirmPage.getAlretsuccess().text  # Get the success message from the alert
        log.info("Text received from application is " + textMatch)  # Log information about the operation
        _capture_screenshot("step8_orderofproducts_screenshot.png", self.driver)  # Capture a screenshot after step 8

        assert ("Success! Thank you!" in textMatch)  # Assert if the success message is as expected
