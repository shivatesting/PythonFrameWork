import os
import configparser
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class TestOne(BaseClass):

    def test_e2e(self, ):
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

        checkoutPage = homePage.checkoutNavs()  # Navigate to the checkout page

        confirmPage = checkoutPage.checkOutItems()  # Proceed with checking out items

        # Log information about the operation
        log.info("Entering country name as " + country_name)

        # Enter the country name ind
        confirmPage.getCountyName().send_keys(country_name)

        self.verifyLinkPresence(country_name_verify)  # Verify if "India" appears in the dropdown

        confirmPage.getcountyNameList().click()  # Select the country from the dropdown

        log.info("Selected country name")  # Log information about the operation
        confirmPage.getAgreeCheckbox().click()  # Agree to the terms by clicking the checkbox
        confirmPage.getPurchaseButton().click()  # Proceed with the purchase by clicking the purchase button
        textMatch = confirmPage.getAlretsuccess().text  # Get the success message from the alert
        log.info("Text received from application is " + textMatch)  # Log information about the operation

        assert ("Success! Thank you!" in textMatch)  # Assert if the success message is as expected
