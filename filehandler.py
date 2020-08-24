
import os, sys

def make_folder_at_dir(target_dir, name):
    try:
        path = os.path.join(target_dir, name)
        os.mkdir(path)
    except OSError as e:
        print(e, file=sys.stderr)
        raise
    finally:
        return path

def get_downloads_directory():
  root_dir = os.path.dirname(os.path.abspath(__file__))
  current_user = os.getlogin()
  idx_for_downloads = root_dir.index(current_user) + len(current_user)
  return f'{root_dir[0:idx_for_downloads]}/Downloads'

def find_by_str(arr, str):
  iterable_arr = iter(arr)
  result = ''
  try:
    result = next(val for val in iterable_arr if str in val and 'csv' in val.lower())
  except StopIteration as e:
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

  amex_csv = find_by_str(filenames, amex_file_key)
  # usaa_csv = find_by_str(filenames, usaa_file_key)
  chase_csv = find_by_str(filenames, chase_file_key)
  
  return [amex_csv, chase_csv]


def main():
  downloads_dir = get_downloads_directory()
  statements = get_statements_from_downloads_dir(downloads_dir)
  print(statements)


  # 1. read from downloads by known file name
  # 2. rename each file to proper type (amex, usaa, chase)
  # 3. make directory in Budget folder by month
  # 4. add 3 files to budget / month folder