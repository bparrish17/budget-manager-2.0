import ezsheets

# Sheet ('Expenses' | 'Incomes' | 'Expenses')
# -- Column ('Date' | 'Amount' | 'Description' | 'Category')


'''
'''
def update_sheet(workbook, sheet_name, sheets_data):
  transaction_list = sheets_data[sheet_name.lower()]
  transaction_list.sort(key=sort_by_date)
  column_names = ['Date', 'Amount', 'Description', 'Category']
  sheet = workbook[sheet_name]
  date_column = sheet.getColumn(1)
  idx_to_add_data = get_last_value_in_data(date_column)

  # update column by column
  for idx, column_name in enumerate(column_names, start=0):
    col_idx = idx + 1 # column indices start at 1 in Google Sheets
    current_column_values = sheet.getColumn(col_idx)[0:idx_to_add_data]
    updated_column = get_new_column_value(column_name, current_column_values, transaction_list)
    sheet.updateColumn(col_idx, updated_column)


def get_new_column_value(
  column_name: str,
  current_column_values: list,
  transactions_list: list
):
  new_column = current_column_values.copy()
  new_values = [transaction[column_name] for transaction in transactions_list]
  new_column.extend(new_values)
  
  return new_column

def sort_by_date(transaction: dict):
  return transaction['Date']

def get_last_value_in_data(column):
  idx_of_last_value = 0
  for idx, cell in enumerate(column, start=1):
    if len(cell) == 0:
      idx_of_last_value = idx
      break

  return idx_of_last_value - 1


def main(sheets_data):
  # test_spreadsheet_id = '1iRHLWOk7E_SPFO_n6Ok0xci__SUtApQGhseuOzz0ThI'
  budget_spreadsheet_id = '1Kwlz2FG-nuHyQM0ieNsUZUfKTpq06OM-wnWcc3LT4Ko'

  workbook = ezsheets.Spreadsheet(budget_spreadsheet_id)
  for sheet_name in ['Expenses', 'Incomes', 'Investments']:
    print(f'Writing {sheet_name.capitalize()} Transactions to Google Sheets...')
    print('-------------------------------------------------------------------------')
    update_sheet(workbook, sheet_name, sheets_data)

  print('\nSuccessfully Written Transactions to Google Sheets\n')
  # expenses_sheet.updateColumn(1, ['test', 'like', 'test', 'val', '----'])
  # new_expenses_column = get_new_column_value(expenses_sheet.getColumn(1), sheets_data['expenses'])
  # expenses_sheet.updateColumn(1, new_expenses_column)
