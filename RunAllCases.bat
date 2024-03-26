@echo off
rem Run test with Allure Report
pytest --alluredir=C:\Users\shiva.chaudhary\PycharmProjects\PythonSelfFramework\pythonProject\allure-results
rem generate Allure report
allure serve C:\Users\shiva.chaudhary\PycharmProjects\PythonSelfFramework\pythonProject\allure-results