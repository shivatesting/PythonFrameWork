import allure
import pytest
from selenium import webdriver
from allure_commons.types import AttachmentType
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from pageObjects.CheckoutPage import CheckOutPage
from pageObjects.HomePage import HomePage
from pageObjects.ConfirmPage import ConfirmPage
from utilities.BaseClass import BaseClass


class TestOne(BaseClass):
    def test_e2e(self):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        checkoutpage = homePage.shopItems()
        log.info("getting all the card titles")
        cards = checkoutpage.getCardTitles()
        i = -1
        for card in cards:
            i = i + 1
            cardText = card.text
            log.info(cardText)
            if cardText == "Blackberry":
                checkoutpage.getCardFooter()[i].click()

        checkoutpage = homePage.checkoutNavs()

        confirmpage = checkoutpage.checkOutItems()
        log.info("Entering country name as ind")

        confirmpage.getCountyName().send_keys("ind")

        self.verifyLinkPresence("India")

        confirmpage.getcountyNameList().click()
        log.info("Selected country name")
        confirmpage.getAgreeCheckbox().click()
        confirmpage.getPurchaseButton().click()
        textMatch = confirmpage.getAlretsuccess().text
        log.info("Text received from application is " + textMatch)

        assert ("Success! Thank you!" in textMatch)
        # testing git code update
