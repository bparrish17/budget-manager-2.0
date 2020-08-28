
import os, sys, shutil
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
    print(f'ERROR: {str} does not exist in {arr[0:5]}...\n')
    raise
  finally:
    return result

def get_statements_from_downloads_dir(downloads_dir):
  amex_file_key = 'activity'
  usaa_file_key = 'bk_download'
  chase_file_key = 'Chase7825'

  filename_list = []

  for (dirpath, dirnames, filenames) in os.walk(downloads_dir):
      filename_list.extend(filenames)
      break

  amex_csv = find_file_by_str(filename_list, amex_file_key)
  usaa_csv = find_file_by_str(filename_list, usaa_file_key)
  chase_csv = find_file_by_str(filename_list, chase_file_key)
  
  return dict({ 'amex': amex_csv, 'usaa': usaa_csv, 'chase': chase_csv })

def rename_files_by_key(root_dir, file_dict):
  new_file_paths = {}

  for file_name in file_dict:
    full_path = f'{root_dir}/{file_dict[file_name]}'
    new_file_name = f'{file_name}.csv'
    new_full_path = f'{root_dir}/{new_file_name}'
    try:
      os.rename(full_path, new_full_path)
    except (NotADirectoryError, OSError) as e:
      print(f'ERROR: renaming file "{file_name}" => {e}\n')
      pass
    finally:
      new_file_paths.update({ new_file_name: new_full_path })

  return new_file_paths

def get_highest_dated_dir(parent_dir, parse_full):
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
      print(f'ERROR: ValueError at {idx} of {dir} in get_highest_dated_dir\n')
      pass
  
  return dir_list[idx_of_highest_val]


def main():
  ROOT_DIR = get_user_root_dir()
  downloads_dir = f'{ROOT_DIR}/Downloads'
  budgeting_dir = f'{ROOT_DIR}/Documents/Home/Budgeting'
  statement_files_dict = get_statements_from_downloads_dir(downloads_dir)

  # change file names
  renamed_statement_files_dict = rename_files_by_key(downloads_dir, statement_files_dict)

  # get highest year directory from /Home/Budgeting => e.g. 2020
  highest_year = get_highest_dated_dir(budgeting_dir, True)
  highest_year_dir = f'{budgeting_dir}/{highest_year}'

  # get highest month directory from /Home/Budgeting/{highestYearDir}
  highest_month = get_highest_dated_dir(highest_year_dir, False)

  # get new month directory to write
  new_month_num = int(highest_month[0]) + 1
  new_month = MONTH_MAP[new_month_num]

  # add new directory
  new_month_dir = make_folder_at_dir(highest_year_dir, f'{new_month_num} - {new_month}')

  # add files to newly created directory
  for file_key in renamed_statement_files_dict:
    file_path = renamed_statement_files_dict[file_key]
    try:
      shutil.move(file_path, f'{new_month_dir}/{file_key}')
    except:
      print(f'ERROR: Could not move {file_key} from {file_path} to "{new_month_dir}/{file_key}"\n')
      pass

  print('Successfully Moved Downloaded Statement Files to Budgeting Folder')
  return new_month_dir

  # 1. read from downloads by known file name
  # 2. rename each file to proper type (amex, usaa, chase)
  # 3. make directory in Budget folder by month
  # 4. add 3 files to budget / month folder


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