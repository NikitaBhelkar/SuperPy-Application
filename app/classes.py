from datetime import datetime
import csv
from config import bought_file,bought_file_copy,sold_file,artificial_date
import pandas as pd
import sys
import shutil
from rich import print


class Product:
    def __init__(self, product_name, buy_price, expiration_date):
         self.product_name = product_name
         self.buy_price = buy_price
         self.expiration_date = expiration_date.strftime('%Y-%m-%d')
    def write_to_boughtcsvfile(self):
         try:
             with open(bought_file, 'a') as f:
                 """ id column in bought_file is incremented for each line"""
                 results = pd.read_csv(bought_file)
                 self.id = len(results) + 1
                 writer = csv.writer(f)
                 # reads the artificial date from text file and uses buy date for product
                 with open(artificial_date, 'r', newline='') as f:
                     date_value = f.readline()
                 buy_date = date_value
                 writer.writerow([self.id, self.product_name, buy_date, self.buy_price, self.expiration_date])
             """creating copy of bought_file for further requirements"""
             shutil.copyfile(bought_file, bought_file_copy)
         except BaseException as e:
            print('BaseException:', e)
         else:
            print('[magenta]OK. Data has been loaded successfully ![/magenta]')

class ProductSell:
    def __init__(self, product_name, sell_price):
        self.product_name = product_name
        self.sell_price = sell_price
      
    def write_to_soldcsvfile(self):
        rownumbers_to_remove = []
        try:
            # reading artificial date value as todays date
            with open(artificial_date, 'r', newline='') as f:
                 expiry_date_value = f.readline()

            df = pd.read_csv(bought_file_copy)
            print("[magenta]bought file dataset - [/magenta]")
            print(df)
            """check if product_name is present in bought products file and expiration_date is greater than today"""
            # filter products from dataset by productname
            df_new = df.loc[df['product_name'] == sys.argv[3]] 
            print("[magenta]dataset containing sold products -[/magenta]")
            print(df_new)
            # filter products from dataset those which are not expired
            df_new_1 = df_new.loc[df_new['expiration_date'] > expiry_date_value]
            print("[magenta]dataset containing sold and not expired products-[/magenta]")
            print(df_new_1)
            if df_new_1.empty:
                print("[magenta]ERROR: Product not in stock.[/magenta]")
            else:
              print("[magenta]OK![/magenta]")

            with open(bought_file_copy, 'r') as fin:
                 reader = csv.reader(fin)
                 for row in reader:
                     """ row is used to check if the list contains any elements before accessing it at an index."""
                     # if conditions checks for product name and expiry date
                     if (row and (row[1] == sys.argv[3]) and (row[4] > expiry_date_value)):
                         bought_id = row[0]
                         rownumbers_to_remove.append(bought_id)
                         with open(sold_file, 'a') as f:
                             """ id column in sold_file is incremented for each line"""
                             results = pd.read_csv(sold_file)
                             id = len(results) + 1
                             writer = csv.writer(f)
                             # reads the artificial date from text file and uses sell date for product
                             with open(artificial_date, 'r', newline='') as f:
                                  date_value = f.readline()
                             sell_date = date_value
                             writer.writerow([id, bought_id,sell_date, self.sell_price]) 
                 df1 = pd.read_csv(bought_file_copy)
                 # considering products other than product_name mentioned in command line argument
                 data = df1.loc[df1['product_name'] != sys.argv[3]]
                 data.to_csv(bought_file_copy, index=False)
            
        except BaseException as e:
            print('BaseException:', e)