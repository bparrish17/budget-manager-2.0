import os, shutil
from FileHandler import main as FileHandler
from FileReader import main as FileReader
from SheetsWriter import main as SheetsWriter
from reset import reset_for_testing

print('-------------------------------------------------------------------------')

new_month_dir = '/Users/brianparrish/Documents/Finance/2021/4 - April'
# new_month_dir = FileHandler()
sheets_data = FileReader(new_month_dir)
SheetsWriter(sheets_data)
# reset_for_testing(new_month_dir)

# reset() < use this for testing

print('-------------------------------------------------------------------------')
