
import csv, os
from math import fabs

def add_csv_data_to_sheets(file_path: str, sheets_data, callback=None) -> list:
  with open(file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      callback(row, sheets_data)

  return sheets_data

def add_amex_row(row, sheets_data):
  amex_data = dict({ 'Date': '', 'Amount': 0, 'Description': '', 'Category': '' })
  amt = float(row['Amount'])

  amex_data['Date'] = row['Date']
  amex_data['Amount'] = fabs(amt)
  amex_data['Description'] = row['Description'].lower().capitalize()
  try:
    amex_data['Category'] = row['Category']
  except KeyError:
    pass
  # todo: 
  # 1. Ignore "ONLINE PAYMENT", incomes?
  # 2. Add categories

  if amt < 0:
    sheets_data['incomes'].append(amex_data)
  else:
    sheets_data['expenses'].append(amex_data)
  
  return sheets_data

def add_chase_row(row, sheets_data):
  chase_data = dict({ 'Date': '', 'Amount': 0, 'Description': '', 'Category': '' })
  
  if row['Type'] != 'Payment':
    amt = float(row['Amount'])
    chase_data['Category'] = row['Category']
    chase_data['Date'] = row['Post Date']
    chase_data['Amount'] = fabs(amt)
    chase_data['Description'] = row['Description'].lower().capitalize()
    if 'games' in chase_data['Description']:
      chase_data['Category'] = 'Entertainment'
    
    sheets_data['expenses'].append(chase_data)

  return sheets_data

def add_usaa_row(row, sheets_data):
  usaa_data = dict({ 'Date': '', 'Amount': 0, 'Description': '', 'Category': '' })
  category = row['Category']
  amt = float(row['Amount'])
  usaa_data['Date'] = row['Date']
  usaa_data['Description'] = row['Description'].lower().capitalize()
  usaa_data['Amount'] = fabs(amt)

  if 'Pending' not in category:
    usaa_data['Category'] = category
  
  if 'icims' in usaa_data['Description'].lower():
    usaa_data['Category'] = 'Paycheck'

  if row['Category'] == 'Credit Card Payment':
    return

  if amt == 1400:
    usaa_data['Category'] = 'Rent'
    usaa_data['Description'] = 'Venmo Rent Payment'


  elif amt < 0:
    if 'Schwab' in usaa_data['Description']:
      # check for account
      if '4547' in usaa_data['Description']:
        row['Category'] = 'Roth'
      elif '7820' in usaa_data['Description']:
        row['Category'] = 'Money Market'
      sheets_data['investments'].append(usaa_data)
    else:
      sheets_data['expenses'].append(usaa_data)

  else:
    sheets_data['incomes'].append(usaa_data)

  return sheets_data

def print_transaction_status(transaction_type: str):
  print(f'Processing {transaction_type.capitalize()} Transactions...')
  print('-------------------------------------------------------------------------')


def main(month_dir: str) -> dict:
  sheets_data = dict({ 'expenses': [], 'incomes': [], 'investments': [] })
  dir_list = os.listdir(month_dir)
  for file in dir_list:
    path = f'{month_dir}/{file}'
    if file == 'amex.csv':
      print_transaction_status('amex')
      add_csv_data_to_sheets(path, sheets_data, add_amex_row)
    elif file == 'chase.csv':
      print_transaction_status('chase')
      add_csv_data_to_sheets(path, sheets_data, add_chase_row)
    elif file == 'usaa.csv':
      print_transaction_status('usaa')
      add_csv_data_to_sheets(path, sheets_data, add_usaa_row)

  return sheets_data

  # read_csv(f'{month_dir}/{dir_list[0]}', read_amex_csv)

