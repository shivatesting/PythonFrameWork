from selenium.webdriver.common.by import By



class ConfirmPage:

    def __init__(self, driver):
        self.driver = driver

    # Locators for various elements on the page
    countyname = (By.ID, "country")
    countynamelist = (By.LINK_TEXT, "India")
    agreecheckbox = (By.XPATH,"//div[@class='checkbox checkbox-primary']")
    purchasebutton = (By.XPATH,"//input[@class='btn btn-success btn-lg']")
    alretsuccess = (By.CLASS_NAME,"alert-success")

    # Method to locate and return the county name element
    def getCountyName(self):
        return self.driver.find_element(*ConfirmPage.countyname)

    # Method to locate and return the county name list element
    def getcountyNameList(self):
        return self.driver.find_element(*ConfirmPage.countynamelist)

    # Method to locate and return the agree checkbox element
    def getAgreeCheckbox(self):
        return self.driver.find_element(*ConfirmPage.agreecheckbox)

    # Method to locate and return the purchase button element
    def getPurchaseButton(self):
        return self.driver.find_element(*ConfirmPage.purchasebutton)

    # Method to locate and return the success alert element
    def getAlretsuccess(self):
        return self.driver.find_element(*ConfirmPage.alretsuccess)





