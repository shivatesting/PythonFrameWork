import os

import openpyxl


class HomePageData:

    @staticmethod
    def getTestData(test_case_name):
        Dict = {}
        current_directory = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_directory, "PythonDemo.xlsx")
        book = openpyxl.load_workbook(file_path)
        sheet = book.active
        for i in range(1, sheet.max_row + 1):
            if sheet.cell(row=i, column=1).value == test_case_name:

                for j in range(2, sheet.max_column + 1):
                    Dict[sheet.cell(row=1, column=j).value] = sheet.cell(row=i, column=j).value
        return [Dict]
