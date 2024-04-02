@echo off

pytest -m smoke --alluredir=C:\Users\shiva.chaudhary\PycharmProjects\PythonSelfFramework\pythonProject\allure-results

allure serve C:\Users\shiva.chaudhary\PycharmProjects\PythonSelfFramework\pythonProject\allure-results

pause