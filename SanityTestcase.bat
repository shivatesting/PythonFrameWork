@echo off

pytest -m sanity --alluredir=C:\Users\shiva.chaudhary\PycharmProjects\PythonSelfFramework\pythonProject\allure-results

allure serve C:\Users\shiva.chaudhary\PycharmProjects\PythonSelfFramework\pythonProject\allure-results

pause