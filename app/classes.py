from datetime import datetime
import csv
from config import bought_file,bought_file_copy,sold_file
import pandas as pd
import sys
import shutil
from rich import print


class Product:
    def __init__(self, product_name, buy_price, expiration_date):
         self.product_name = product_name
         self.buy_price = buy_price
         self.expiration_date = expiration_date.strftime('%Y-%m-%d')
         self.buy_date = datetime.now().strftime('%Y-%m-%d')

    def write_to_boughtcsvfile(self):
         try:
             with open(bought_file, 'a', newline='') as f:
                 """ id column in bought_file is incremented for each line"""
                 results = pd.read_csv(bought_file)
                 self.id = len(results) + 1
                 writer = csv.writer(f)
                 writer.writerow([self.id, self.product_name, self.buy_date, self.buy_price, self.expiration_date])
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
        self.sell_date = datetime.now().strftime('%Y-%m-%d')
      
    def write_to_soldcsvfile(self):
        rownumbers_to_remove = []
        try:
            df = pd.read_csv(bought_file_copy)
            """check if product_name is present in bought products file"""
            df = df.loc[df['product_name'] == sys.argv[3]]
            with open(bought_file_copy, 'r', newline='') as fin:
                 reader = csv.reader(fin)
                 for row in reader:
                     """ row is used to check if the list contains any elements before accessing it at an index."""
                     if (row and row[1] == 'orange'):
                         bought_id = row[0]
                         rownumbers_to_remove.append(bought_id)
                         with open(sold_file, 'a', newline='') as f:
                             """ id column in sold_file is incremented for each line"""
                             results = pd.read_csv(sold_file)
                             id = len(results) + 1
                             writer = csv.writer(f)
                             writer.writerow([id, bought_id, self.sell_date, self.sell_price]) 
                 df1 = pd.read_csv(bought_file_copy)
                 """ removing sold products from bought products to get current inventory details after selling products """
                 # considering products other than product_name mentioned in command line argument
                 data = df1.loc[df1['product_name'] != sys.argv[3]]
                 data.to_csv(bought_file_copy, index=False)
            if df.empty:
                print("[magenta]ERROR: Product not in stock.[/magenta]")
            else:
                print("[magenta]OK![/magenta]")
        except BaseException as e:
            print('BaseException:', e)
        
