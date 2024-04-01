from selenium.webdriver.common.by import By
from pageObjects.CheckoutPage import CheckOutPage

class HomePage:

    def __init__(self, driver):
        self.driver = driver

    # Locators for various elements on the page
    shop = (By.CSS_SELECTOR, "a[href*='shop']")
    name = (By.CSS_SELECTOR, "[name='name']")
    email = (By.NAME, "email")
    check = (By.ID, "exampleCheck1")
    gender = (By.ID, "exampleFormControlSelect1")
    submit = (By.XPATH, "//input[@value='Submit']")
    successMessage = (By.CSS_SELECTOR, "[class*='alert-success']")
    checkoutNav = (By.XPATH, "//a[@class='nav-link btn btn-primary']")

    # Method to navigate to the shop page and return a CheckOutPage object
    def shopItems(self):
        self.driver.find_element(*HomePage.shop).click()
        checkOutPage = CheckOutPage(self.driver)
        return checkOutPage

    # Methods to locate specific elements on the page
    def getName(self):
        return self.driver.find_element(*HomePage.name)

    def getEmail(self):
        return self.driver.find_element(*HomePage.email)

    def getCheckBox(self):
        return self.driver.find_element(*HomePage.check)

    def getGender(self):
        return self.driver.find_element(*HomePage.gender)

    def submitForm(self):
        return self.driver.find_element(*HomePage.submit)

    def getSuccessMessage(self):
        return self.driver.find_element(*HomePage.successMessage)

    # Method to navigate to the checkout page and return a CheckOutPage object
    def checkoutNavs(self):
        self.driver.find_element(*HomePage.checkoutNav).click()
        checkOutPage = CheckOutPage(self.driver)
        return checkOutPage
