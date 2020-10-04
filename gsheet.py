import pygsheets
import pandas as pd

gc = pygsheets.authorize(service_file='<downloaded-json-file>.json')

res = gc.sheet.create("dashboard_data")
created_spreadsheet = gc.open_by_key(res['spreadsheetId'])
created_spreadsheet.share('<your>@gmail.com', role='writer', type='user', )
created_spreadsheet.share('', role='reader', type='anyone')


df = pd.read_csv('orders.csv', encoding='utf8')
df["turnover"] = df["turnover"].astype(float)
df["quantity"] = df["quantity"].astype(float)


sales_per_country = df[["turnover", "quantity","country"]].groupby("country").agg("sum").reset_index()
sales_per_category = df[["turnover", "quantity","categoryname"]].groupby("categoryname").agg("sum").reset_index()
sales_per_year = df[["turnover", "quantity","year"]].groupby("year").agg("sum").reset_index()

wks = created_spreadsheet.sheet1
wks.title = 'sales_per_country'
wks.set_dataframe(sales_per_country, start=(1,1))

wks = created_spreadsheet.add_worksheet("sales_per_category")
wks.set_dataframe(sales_per_category, start=(1,1))

wks = created_spreadsheet.add_worksheet("sales_per_year")
wks.set_dataframe(sales_per_year, start=(1,1))

print(f"sheet id: {created_spreadsheet.id}")