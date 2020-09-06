import ezsheets


# Sheet ('Expenses' | 'Incomes' | 'Expenses')
# -- Column ('Date' | 'Amount' | 'Description' | 'Category')

def update_sheet(workbook, sheet_name: str, sheets_data: dict):
    """
    Update Workbook Sheet With Transactions

    Args:
        workbook: Google Sheets Folder
        sheet_name ('Expenses' | 'Incomes' | 'Expenses'): Sheet Tab in Google Sheets Folder
        sheets_data (dict): dict of sheets_data keyd by sheet_name

    Returns:
        void

    """
    transaction_list = sheets_data[sheet_name.lower()]
    transaction_list.sort(key=sort_by_date)
    column_names = ['Date', 'Amount', 'Description', 'Category']
    sheet = workbook[sheet_name]
    date_column = sheet.getColumn(1)
    idx_to_add_data = get_last_value_in_data(date_column)

    # update column by column
    for idx, column_name in enumerate(column_names, start=0):
        col_idx = idx + 1  # column indices start at 1 in Google Sheets
        current_column_values = sheet.getColumn(col_idx)[0:idx_to_add_data]
        updated_column = get_new_column_value(column_name, current_column_values, transaction_list)
        sheet.updateColumn(col_idx, updated_column)


def get_new_column_value(
        column_name: str,
        current_column_values: list,
        transactions_list: list
):
    """
    Combines existing column values with new values from transactions
    Args:
        column_name ('Date' | 'Amount' | 'Description' | 'Category'): name of column to read
        current_column_values (list<str>):
        transactions_list (dict): transactions from CSV

    Returns:
        new_column: New combined list of column values
    """
    new_column = current_column_values.copy()
    new_values = [transaction[column_name] for transaction in transactions_list]
    new_column.extend(new_values)

    return new_column


def sort_by_date(transaction: dict) -> str:
    return transaction['Date']


def get_last_value_in_data(column: list) -> int:
    """
    Gets
    Args:
        column (list):

    Returns (int):
        index of last row that has a value in that column
    """
    idx_of_last_value = 0
    for idx, cell in enumerate(column, start=1):
        if len(cell) == 0:
            idx_of_last_value = idx
            break

    return idx_of_last_value - 1


def main(sheets_data: dict):
    """
    Iterates over each sheet and appends transactions
    Args:
        sheets_data (dict): existing transactions to add to sheets
    """
    # test_spreadsheet_id = '1iRHLWOk7E_SPFO_n6Ok0xci__SUtApQGhseuOzz0ThI'
    budget_spreadsheet_id = '1Kwlz2FG-nuHyQM0ieNsUZUfKTpq06OM-wnWcc3LT4Ko'

    workbook = ezsheets.Spreadsheet(budget_spreadsheet_id)
    for sheet_name in ['Expenses', 'Incomes', 'Investments']:
        print(f'Writing {sheet_name} Transactions to Google Sheets...')
        print('-------------------------------------------------------------------------')
        update_sheet(workbook, sheet_name, sheets_data)

    print('\nSuccessfully Written Transactions to Google Sheets\n')
