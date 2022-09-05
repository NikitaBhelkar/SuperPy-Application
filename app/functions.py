
from classes import Product, ProductSell
from config import bought_file,bought_file_copy,sold_file,artificial_date
import sys
from datetime import date, timedelta, datetime
import pandas as pd
"""used to avoid SettingWithCopy warning"""
pd.set_option('mode.chained_assignment', None)
from rich import print
from tabulate import tabulate


def buy_product(args):
    try:
        Product(args.product_name, args.price, args.expiration_date).write_to_boughtcsvfile()
    except Exception as e:
        print(e)

def sell_product(args):
    try:
        ProductSell(args.product_name, args.price).write_to_soldcsvfile()
    except Exception as e:
        print(e)

def advance_time(args):
    try:
        today_date = date.today()
        today_date_strformat = today_date.strftime('%Y-%m-%d')
        print("[magenta]Today_date :[/magenta]"+today_date_strformat)
        #adding today's date  to artificial_date.txt file for the first time if the text file is empty
        with open(artificial_date, 'r+', newline='') as f:
             content = f.readline()
             if content == "":
                 f.write(today_date_strformat)
        if args.advance_time == None:
            return today_date
        else:
            td = timedelta(int(sys.argv[2]))
            # opens artificial_date.txt and reads date value from it 
            with open(artificial_date, 'r', newline='') as f:
                 date_value = f.readline()
                 print("[magenta]date_value from artificial_date.txt file:[/magenta]"+ date_value)
                 # converting date_value in date format
                 dt = datetime.strptime(date_value, '%Y-%m-%d')
            # adding timedelta value to date
            artificial_date_value = (dt + td).strftime('%Y-%m-%d')
            print("[magenta]artificial_date :[/magenta]"+ artificial_date_value)
            # writes the advanced date to artificial_date.txt 
            with open(artificial_date, 'w', newline='') as f1:
               f1.write(artificial_date_value)
            return artificial_date_value
    except Exception as e:
        print(e)

def report_inventory(args):
     df = pd.read_csv(bought_file_copy)
     # reading today_date value from artificial_date text file 
     with open(artificial_date, 'r', newline='') as f:
         date_value = f.readline()
     if args.now == True :
         # considering values in dataset till today
         data_set_now = df.loc[df['buy_date'] <= date_value ]
         if data_set_now.empty :
             print("[magenta]No products available[/magenta]")
         else:
             # groupby product_name,buy_date to get the count of no of products
             data_set_now['count'] = data_set_now.groupby(['product_name','buy_date','expiration_date'])['id'].transform('count')
             data_set = data_set_now.drop(['id','buy_price'],axis = 1).drop_duplicates()
             # displaying data in tabular format
             print(tabulate([data_set.columns.values.tolist()] + data_set.values.tolist(), headers='firstrow', tablefmt='grid'))
     elif args.yesterday == True:
         # considering values in dataset till yesterday
         data_set_yesterday = df.loc[df['buy_date'] < date_value]
         if data_set_yesterday.empty :
             print("[magenta]No products available[/magenta]")
         else:
             # groupby product_name,expiration_date,buy_date to get the count of no of products
             data_set_yesterday['count'] = data_set_yesterday.groupby(['product_name','expiration_date','buy_date'])['id'].transform('count')
             data_set = data_set_yesterday.drop(['id','buy_date'],axis = 1).drop_duplicates()
             print(tabulate([data_set.columns.values.tolist()] + data_set.values.tolist(), headers='firstrow', tablefmt='grid'))

def get_sold_product_details(df):
     # groupby sell_date,sell_price to get the count of sold products
     df['count']= df.groupby(['sell_date','sell_price'])['bought_id'].transform('count').drop_duplicates()
     df['revenue_per_product'] = df['sell_price']*df['count']
     print(df['revenue_per_product'])
     total_revenue = df['revenue_per_product'].sum()  
     print(total_revenue)   
     return total_revenue

def report_revenue(args):
     # reading today_date value from artificial_date text file 
     with open(artificial_date, 'r', newline='') as f:
         date_value = f.readline()
     df = pd.read_csv(sold_file,on_bad_lines='skip')
     if args.yesterday == True:
         # considering values in dataset till yesterday
         data_set_yesterday = df.loc[df['sell_date'] < str(date_value)]
         if data_set_yesterday.empty:
             print("[magenta]Yesterday's revenue: 0[/magenta]")
         else:
             total_revenue = get_sold_product_details(data_set_yesterday)
             print("[magenta]Yesterday's revenue: [/magenta]",total_revenue)
     if args.today == True:
         # considering values in dataset where sell_date date_value
         data_set_today = df.loc[df['sell_date'] == str(date_value)]
         if data_set_today.empty:
             print("[magenta]Today's revenue so far: 0[/magenta]")
         else:
             total_revenue = get_sold_product_details(data_set_today)
             print("[magenta]Today's revenue so far: [/magenta]",total_revenue)
     if args.date != None :
         # convert args.date in '%Y-%m' format
         given_date_input = str((args.date).strftime('%Y-%m'))
         date_time_obj = datetime.strptime(given_date_input,"%Y-%m")
         month = date_time_obj.month
         year = date_time_obj.year
         monthDict = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
         month_value = monthDict.get(month)
         # change sell_date value to '%Y-%m' format
         df['sell_date'] = pd.to_datetime(df.sell_date, format='%Y-%m')
         df['sell_date'] = df.sell_date.dt.strftime('%Y-%m')
         # consider data where sell_date values == given_date_input
         dataset_date = df.loc[df['sell_date'] == str(given_date_input)]
         if dataset_date.empty:
             print("[magenta]Revenue from [/magenta]",month_value ,year ,"[magenta]:[/magenta] ", "0")
         else:
             total_revenue = get_sold_product_details(dataset_date)
             print("[magenta]Revenue from [/magenta]",month_value ,year ,"[magenta]:[/magenta]",total_revenue)

def report_profit(args):
     # reading today_date value from artificial_date text file 
     with open(artificial_date, 'r', newline='') as f:
         date_value = f.readline()
     df = pd.read_csv(sold_file,on_bad_lines='skip')
     # considering values in dataset where sell_date == date_value
     data_set_today = df.loc[df['sell_date'] == str(date_value)]
     bought_id_value_list = data_set_today['bought_id'].to_list()
     if data_set_today.empty:
         revenue_of_total_products_sold = 0
     else:
         revenue_of_total_products_sold = get_sold_product_details(data_set_today)
     print("revenue_of_total_products_sold :",revenue_of_total_products_sold)
     df = pd.read_csv(bought_file,on_bad_lines='skip')
     # considering values in dataset where buy_date == date_value 
     data_set = df.loc[df['buy_date'] == str(date_value)]
     if data_set.empty:
         revenue_of_total_products_bought = 0
     else:
         dataset_bought_products_detail = data_set.loc[df['id'].isin(bought_id_value_list)]
         products_bought_list = dataset_bought_products_detail['buy_price'].to_list()
         print("products_bought_list-", products_bought_list)
         total = 0
         for ele in range(0, len(products_bought_list)):
             total = total + products_bought_list[ele]
     print("revenue_of_total_products_bought :", total)
     profit_percent = (revenue_of_total_products_sold - total)
     print("[magenta]profit_percent :[/magenta]",profit_percent)
     
     


