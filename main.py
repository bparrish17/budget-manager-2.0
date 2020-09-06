import os, shutil
from filehandler import main as filehandler
from filereader import main as filereader
from sheetswriter import main as sheetswriter
from reset import main as reset

print('-------------------------------------------------------------------------')

# new_month_dir = '/Users/brianparrish/Documents/Home/Budgeting/2020/8 - August'
new_month_dir = filehandler()
sheets_data = filereader(new_month_dir)
sheetswriter(sheets_data)

# reset() < use this for testing

print('-------------------------------------------------------------------------')
