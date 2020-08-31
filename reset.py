
import os, shutil

def RESET_FOR_TESTING(new_month_dir):
  dir_list = os.listdir(new_month_dir)
  for file_key in dir_list:
    try:
      print(f'{new_month_dir}/{file_key}', '=> ', f'/Users/brianparrish/Downloads/{file_key}')
      shutil.move(f'{new_month_dir}/{file_key}', f'/Users/brianparrish/Downloads/{file_key}')
    except:
      print(f'ERROR: Could not move {file_key}"\n')
      pass

  shutil.rmtree(new_month_dir)

def main():
  new_month_dir = '/Users/brianparrish/Documents/Home/Budgeting/2020/8 - August'
  RESET_FOR_TESTING(new_month_dir)
  print('Reset Successful')