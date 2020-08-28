# import ezsheets
import os, shutil
from filehandler import main as filehandler, RESET_FOR_TESTING

# test_spreadsheet_id = '1iRHLWOk7E_SPFO_n6Ok0xci__SUtApQGhseuOzz0ThI'
# spreadsheet = ezsheets.Spreadsheet(test_spreadsheet_id)
# expenses_sheet = spreadsheet['Expenses']
# expenses_sheet.updateColumn(1, ['shawty', 'like', 'a melody', 'in my', 'head'])

# print(expenses_sheet)
new_month_dir = filehandler()
# new_month_dir = '/Users/brianparrish/Documents/Home/Budgeting/2020/8 - August'
# RESET_FOR_TESTING(new_month_dir)

print('Success')
