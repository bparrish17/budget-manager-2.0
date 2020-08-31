import ezsheets

# Sheet ('Expenses' | 'Incomes' | 'Expenses')
# -- Column ('Date' | 'Amount' | 'Description' | 'Category')

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
    new_column = get_new_column_value(column_name, sheet_column, transaction_list)
    sheet.updateColumn(col_idx, new_column)

    print('-----------------------------------')
    print(new_column)

def get_new_column_value(column_name, current_column_values, transactions):
  lastIndex = get_last_value_in_column(current_column_values)
  sliced = current_column_values[0:lastIndex]
  new_values = [transaction[column_name] for transaction in transactions]
  sliced.extend(new_values)
  
  return sliced


def get_last_value_in_column(column):
  idx_of_last_value = 0
  for idx, cell in enumerate(column, start=0):
    if len(cell) == 0:
      idx_of_last_value = idx
      break

  return idx_of_last_value


def main(sheets_data):
  test_spreadsheet_id = '1iRHLWOk7E_SPFO_n6Ok0xci__SUtApQGhseuOzz0ThI'
  workbook = ezsheets.Spreadsheet(test_spreadsheet_id)
  for sheet_name in ['Expenses', 'Incomes', 'Investments']:
    update_sheet(workbook, sheet_name, sheets_data)

  print(sheets_data)
  # expenses_sheet.updateColumn(1, ['test', 'like', 'test', 'val', '----'])
  # new_expenses_column = get_new_column_value(expenses_sheet.getColumn(1), sheets_data['expenses'])
  # expenses_sheet.updateColumn(1, new_expenses_column)
