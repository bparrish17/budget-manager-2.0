import ezsheets

# Sheet ('Expenses' | 'Incomes' | 'Expenses')
# -- Column ('Date' | 'Amount' | 'Description' | 'Category')


# LEFT OFF: refactoring update_sheet to only go off first column as source of truth (in case there's missing categories or amounts or whatever)
'''
'''
def update_sheet(workbook, sheet_name, sheets_data):
  transaction_list = sheets_data[sheet_name.lower()]
  column_names = ['Date', 'Amount', 'Description', 'Category']
  sheet = workbook[sheet_name]
  for idx, column_name in enumerate(column_names, start=0):
    col_idx = idx + 1
    # update column by column
    sheet_column = sheet.getColumn(col_idx)
    idx_to_add_data = get_last_value_in_data(sheet_column)
    new_column = get_new_column_value(column_name, idx_to_add_data, sheets_column, transaction_list)
    sheet.updateColumn(col_idx, new_column)



def get_new_column_value(
  column_name: str,
  idx_to_add_data: int,
  transactions
):
  sliced = current_column_values[0:idx_to_add_data]
  new_values = [transaction[column_name] for transaction in transactions]
  sliced.extend(new_values)
  
  return sliced


def get_last_value_in_data(column):
  idx_of_last_value = 0
  for idx, cell in enumerate(column, start=1):
    if len(cell) == 0:
      idx_of_last_value = idx
      break

  print('SHAWTY: ', idx_of_last_value, column[idx_of_last_value])
  return idx_of_last_value

def print_sheet_status(sheet_name: str):
  print(f'Writing {sheet_name.capitalize()} Transactions to Google Sheets...')
  print('-------------------------------------------------------------------------')

def main(sheets_data):
  # test_spreadsheet_id = '1iRHLWOk7E_SPFO_n6Ok0xci__SUtApQGhseuOzz0ThI'
  budget_spreadsheet_id = '1Kwlz2FG-nuHyQM0ieNsUZUfKTpq06OM-wnWcc3LT4Ko'

  workbook = ezsheets.Spreadsheet(budget_spreadsheet_id)
  for sheet_name in ['Expenses', 'Incomes', 'Investments']:
    print_sheet_status(sheet_name)
    update_sheet(workbook, sheet_name, sheets_data)

  print('\nSuccessfully Written Transactions to Google Sheets\n')
  # expenses_sheet.updateColumn(1, ['test', 'like', 'test', 'val', '----'])
  # new_expenses_column = get_new_column_value(expenses_sheet.getColumn(1), sheets_data['expenses'])
  # expenses_sheet.updateColumn(1, new_expenses_column)
