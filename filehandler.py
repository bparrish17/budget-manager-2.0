import os, sys, shutil
from constants import MONTH_MAP
from MonthDirectoryFinder import main as get_highest_month_dir


def make_folder_at_dir(target_dir: str, name: str) -> str:
    """
    Creates directory inside target parent directory by name
    Args:
        target_dir (str): directory to add folder to
        name (str): name of directory to add

    Returns:
        Path of newly created folder
    """
    try:
        path = os.path.join(target_dir, name)
        os.mkdir(path)
    except OSError as e:
        print(e, file=sys.stderr)
        raise
    finally:
        return path


def find_file_by_str(arr: list, string: str) -> str:
    """
    Finds file in list of files by string name
    Args:
        arr (list): list of files to look through
        string (str): file name to look for

    Returns (str):
        Path of found file
    """
    iterable_arr = iter(arr)
    result = ''
    try:
        result = next(val for val in iterable_arr if string in val and 'csv' in val.lower())
    except StopIteration:
        print(f'ERROR: {string} does not exist in {arr[0:5]}...\n')
        raise
    finally:
        return result


def get_statements_from_downloads_dir(downloads_dir: str) -> dict:
    """
    Find the download financial statement CSVs in the expected directory
    Args:
        downloads_dir (str): OS downloads directory to look for statements

    Returns (dict):
        Dictionary of renamed financial statements keyed by their file name
    """
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

    return dict({'amex': amex_csv, 'usaa': usaa_csv, 'chase': chase_csv})


def rename_files_by_key(parent_dir, file_dict):
    """
    For each provided file in dict, rename them in their current parent directory
    Args:
      parent_dir (str): root directory for user (MacOS) (e.g. Users/<name>)
      file_dict (dict<{ amex: str, usaa: str, chase: str }): dict with each csv path

    Returns (dict):
      Dict keyed by file name with value of the new path of that file
    """
    new_file_paths = {}

    for file_name in file_dict:
        full_path = f'{parent_dir}/{file_dict[file_name]}'
        new_file_name = f'{file_name}.csv'
        new_full_path = f'{parent_dir}/{new_file_name}'
        try:
            os.rename(full_path, new_full_path)
        except (NotADirectoryError, OSError) as e:
            print(f'ERROR: renaming file "{file_name}" => {e}\n')
            pass
        finally:
            new_file_paths.update({new_file_name: new_full_path})

    return new_file_paths

def main() -> str:
    """
    File Handler for Downloaded CSVs
    1. Find downloaded financial statements by each file key
    2. Renames files in place
    3. Find latest month directory, then create one for next month (e.g. 8 - August)
    4. Move renamed financial statement files to newly created month directory

    Returns (str):
      String path of new month directory (e.g. /Users/<name>/Documents/Home/Budgeting/8 - August)
    """
    root_dir = get_user_root_dir()
    downloads_dir = f'{root_dir}/Downloads'
    budgeting_dir = f'{root_dir}/Documents/Finance'
    statement_files_dict = get_statements_from_downloads_dir(downloads_dir)

    # change file names
    renamed_statement_files_dict = rename_files_by_key(downloads_dir, statement_files_dict)

    # get highest year directory from /Home/Budgeting => e.g. 2020
    highest_year = get_highest_dated_dir(budgeting_dir, True)
    highest_year_dir = f'{budgeting_dir}/{highest_year}'

    (highest_year_dir_name, new_month_dir_name) = get_highest_month_dir()

    # get highest month directory from /Home/Budgeting/{highestYearDir}
    highest_month = get_highest_dated_dir(highest_year_dir, False)

    # get new month directory to write
    new_month_num = int(highest_month[0]) + 1
    new_month = MONTH_MAP[new_month_num]

    # add new directory
    new_month_dir = make_folder_at_dir(highest_year_dir_name, new_month_dir_name)

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

def main_2():
    root_dir = get_user_root_dir()
    downloads_dir = f'{root_dir}/Downloads'

    # Rename downloaded transaction files to expected names
    statement_files_dict = get_statements_from_downloads_dir(downloads_dir)
    renamed_statement_files_dict = rename_files_by_key(downloads_dir, statement_files_dict)

    # Get month directory to add renamed files to
    (highest_year_dir_name, new_month_dir_name) = get_highest_month_dir()
    new_month_dir = make_folder_at_dir(highest_year_dir_name, new_month_dir_name)

    for file_key in renamed_statement_files_dict:
        file_path = renamed_statement_files_dict[file_key]
        try:
            shutil.move(file_path, f'{new_month_dir}/{file_key}')
        except:
            print(f'ERROR: Could not move {file_key} from {file_path} to "{new_month_dir}/{file_key}"\n')
            pass

    print('Successfully Moved Downloaded Statement Files to Budgeting Folder')