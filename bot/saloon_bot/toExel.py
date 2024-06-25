import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from sqlalchemy import create_engine

# Аутентификация в Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('', scope)
gc = gspread.authorize(credentials)

# Получение данных из Google Sheets
spreadsheet_key = '
worksheet_name = ''
worksheet = gc.open_by_key(spreadsheet_key).worksheet(worksheet_name)
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])  # Преобразование в DataFrame

# Экспорт данных в файл Excel
df.to_excel('data.xlsx', index=False)

# Обработка данных (пример)
df['new_column'] = df['old_column'] * 2

# Экспорт обработанных данных в базу данных
engine = create_engine('sqlite:///data.db')  # Создание SQLite базы данных
df.to_sql('table_name', engine, if_exists='replace', index=False)

# Извлечение данных из базы данных
query = 'SELECT * FROM table_name'
df_from_db = pd.read_sql_query(query, engine)

# Экспорт данных из базы данных в файл Excel
df_from_db.to_excel('processed_data.xlsx', index=False)

# Загрузка обновленных данных обратно в Google Sheets
processed_data = pd.read_excel('processed_data.xlsx')
worksheet.update([processed_data.columns.values.tolist()] + processed_data.values.tolist())
