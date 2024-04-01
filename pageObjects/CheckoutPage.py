from selenium.webdriver.common.by import By
from pageObjects.ConfirmPage import ConfirmPage


class CheckOutPage:

    def __init__(self, driver):
        self.driver = driver

    # Locators for various elements on the page
    cardTitle = (By.CSS_SELECTOR, ".card-title a")
    cardFooter = (By.CSS_SELECTOR, ".card-footer button")
    checkOut = (By.XPATH, "//button[@class='btn btn-success']")

    # Method to locate and return a list of card titles
    def getCardTitles(self):
        return self.driver.find_elements(*CheckOutPage.cardTitle)

    # Method to locate and return a list of card footers
    def getCardFooter(self):
        return self.driver.find_elements(*CheckOutPage.cardFooter)

    # Method to click on the checkout button and return a ConfirmPage object
    def checkOutItems(self):
        self.driver.find_element(*CheckOutPage.checkOut).click()
        confirmPage = ConfirmPage(self.driver)
        return confirmPage
