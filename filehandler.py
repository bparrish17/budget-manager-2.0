
import os, sys
from constants import MONTH_MAP

def make_folder_at_dir(target_dir, name):
    try:
        path = os.path.join(target_dir, name)
        os.mkdir(path)
    except OSError as e:
        print(e, file=sys.stderr)
        raise
    finally:
        return path

def get_user_root_dir():
  root_dir = os.path.dirname(os.path.abspath(__file__))
  current_user = os.getlogin()
  idx_for_downloads = root_dir.index(current_user) + len(current_user)
  return f'{root_dir[0:idx_for_downloads]}'

def find_file_by_str(arr, str):
  iterable_arr = iter(arr)
  result = ''
  try:
    result = next(val for val in iterable_arr if str in val and 'csv' in val.lower())
  except StopIteration:
    print(f'Err: {str} does not exist in {arr}')
    raise
  finally:
    return result

def get_statements_from_downloads_dir(downloads_dir):
  amex_file_key = 'activity'
  usaa_file_key = 'bk_download'
  chase_file_key = 'Chase7825'

  file_list = []

  for (dirpath, dirnames, filenames) in os.walk(downloads_dir):
      file_list.extend(filenames)
      break

  amex_csv = find_file_by_str(filenames, amex_file_key)
  usaa_csv = find_file_by_str(filenames, usaa_file_key)
  chase_csv = find_file_by_str(filenames, chase_file_key)
  
  return [amex_csv, usaa_csv, chase_csv]

def get_latest_dated_dir(parent_dir, parse_full):
  dir_list = os.listdir(parent_dir)
  highest_val = 0
  idx_of_highest_val = 0

  for idx, dir in enumerate(dir_list, start=0):
    try:
      if (parse_full == True):
        curr_val = int(dir)
      else:
        curr_val = int(dir[0])

      if (curr_val > highest_val):
        highest_val = curr_val
        idx_of_highest_val = idx
    except ValueError:
      pass
  
  return dir_list[idx_of_highest_val]


def main():
  ROOT_DIR = get_user_root_dir()
  downloads_dir = f'{ROOT_DIR}/Downloads'
  statement_files = get_statements_from_downloads_dir(downloads_dir)
  budgeting_dir = f'{ROOT_DIR}/Documents/Home/Budgeting'
  # get highest year directory from /Home/Budgeting => e.g. 2020
  year_dir = f'{budgeting_dir}/{get_latest_dated_dir(budgeting_dir, True)}'
  # get highest month directory from /Home/Budgeting/{highestYearDir}
  month_dir = f'{year_dir}/{get_latest_dated_dir(year_dir, False)}'
  # change file names
  print(MONTH_MAP[1])
  print(month_dir)


  # 1. read from downloads by known file name
  # 2. rename each file to proper type (amex, usaa, chase)
  # 3. make directory in Budget folder by month
  # 4. add 3 files to budget / month folder