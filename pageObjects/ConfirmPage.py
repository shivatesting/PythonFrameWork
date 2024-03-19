from selenium.webdriver.common.by import By



class ConfirmPage:

    def __init__(self, driver):
        self.driver = driver

    countyname = (By.ID, "country")
    countynamelist = (By.LINK_TEXT, "India")
    agreecheckbox = (By.XPATH,"//div[@class='checkbox checkbox-primary']")
    purchasebutton = (By.XPATH,"//input[@class='btn btn-success btn-lg']")
    alretsuccess = (By.CLASS_NAME,"alert-success")


    def getCountyName(self):
        return self.driver.find_element(*ConfirmPage.countyname)

    def getcountyNameList(self):
        return self.driver.find_element(*ConfirmPage.countynamelist)

    def getAgreeCheckbox(self):
        return self.driver.find_element(*ConfirmPage.agreecheckbox)

    def getPurchaseButton(self):
        return self.driver.find_element(*ConfirmPage.purchasebutton)

    def getAlretsuccess(self):
        return self.driver.find_element(*ConfirmPage.alretsuccess)





