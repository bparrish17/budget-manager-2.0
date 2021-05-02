import os, sys, shutil
from constants import MONTH_MAP
from utils import get_user_root_dir

def get_highest_dated_dir(parent_dir, parse_full) -> str:
    """
    Get the latest dated directory in existing Budgeting folder
    Args:
      parent_dir (str): directory to parse through
      parse_full (bool): whether or not parse full directory list

    Returns (str):
      Highest dated directory in parent directory (e.g. '8 - August')
    """
    dir_list = os.listdir(parent_dir)
    highest_val = 0
    idx_of_highest_val = 0

    for idx, directory in enumerate(dir_list, start=0):
        try:
            if parse_full:
                curr_val = int(directory)
            else:
                curr_val = int(directory[0])

            if curr_val > highest_val:
                highest_val = curr_val
                idx_of_highest_val = idx
        except ValueError:
            print(f'ERROR: ValueError at {idx} of {directory} in get_highest_dated_dir\n')
            pass

    return dir_list[idx_of_highest_val]


def main() -> tuple:
    """
    Finds new month directory to put downloaded files in
    - Finds highest existing directory (e.g. "2 - February" that was added last month)

    Returns (tuple<str>):
      String path of month directory where downloads will go
      (e.g. /Users/<name>/Documents/Finance/2021/3 - March)
    """
    root_dir = get_user_root_dir()
    downloads_dir = f'{root_dir}/Downloads'
    budgeting_dir = f'{root_dir}/Documents/Finance'

    # get highest year directory from /Finance => e.g. 2020
    highest_year = get_highest_dated_dir(budgeting_dir, True)
    highest_year_dir = f'{budgeting_dir}/{highest_year}'

    # get highest month directory from /Home/Budgeting/{highestYearDir}
    highest_month = get_highest_dated_dir(highest_year_dir, False)

    # get new month directory
    new_month_num = int(highest_month[0]) + 1
    new_month = MONTH_MAP[new_month_num]

    highest_month_dir = f'{new_month_num} - {new_month}'

    return (highest_year_dir, highest_month_dir)
