
from classes import Product, ProductSell
from config import bought_file,bought_file_copy,sold_file
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
        if args.advance_time == None:
            return today_date
        else:
            td = timedelta(int(sys.argv[2]))
            artificial_date = (today_date + td).strftime('%Y-%m-%d')
            print("[magenta]artificial_date :[/magenta]"+ artificial_date)
            return artificial_date
    except Exception as e:
        print(e)

def report_inventory(args):
     df = pd.read_csv(bought_file_copy)
     #calling advance_time function to get current date 
     today_date = advance_time(args)
     if args.now == True :
         # considering values in dataset till today
         data_set_now = df.loc[df['buy_date'] <= str(today_date)]
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
         data_set_yesterday = df.loc[df['buy_date'] < str(today_date)]
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
     total_revenue = df['revenue_per_product'].sum()     
     return total_revenue

def report_revenue(args):
     #calling advance_time function to get current date 
     today_date = advance_time(args)
     df = pd.read_csv(sold_file,on_bad_lines='skip')
     if args.yesterday == True:
         # considering values in dataset till yesterday
         data_set_yesterday = df.loc[df['sell_date'] < str(today_date)]
         if data_set_yesterday.empty:
             print("[magenta]Yesterday's revenue: 0[/magenta]")
         else:
             total_revenue = get_sold_product_details(data_set_yesterday)
             print("[magenta]Yesterday's revenue: [/magenta]",total_revenue)
     if args.today == True:
         # considering values in dataset where sell_date is today's date
         data_set_today = df.loc[df['sell_date'] == str(today_date)]
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


def get_bought_product_details(data_set):
     #groupby product_name,buy_price to get the count of bought products
     data_set['count']= data_set.groupby(['product_name','buy_price'])['buy_date'].transform('count')
     data_set = data_set.drop(["id"],axis = 1).drop_duplicates()
     data_set['revenue_per_product'] = data_set['buy_price']*data_set['count']
     revenue_of_total_products_bought= data_set['revenue_per_product'].sum()  
     return revenue_of_total_products_bought

def report_profit(args):
     #calling advance_time function to get current date 
     today_date = advance_time(args)
     df = pd.read_csv(sold_file,on_bad_lines='skip')
     # considering values in dataset where sell_date == today_date
     data_set_today = df.loc[df['sell_date'] == str(today_date)]
     if data_set_today.empty:
         revenue_of_total_products_sold = 0
     else:
         revenue_of_total_products_sold = get_sold_product_details(data_set_today)
     df = pd.read_csv(bought_file,on_bad_lines='skip')
     # considering values in dataset where buy_date == today_date
     data_set = df.loc[df['buy_date'] == str(today_date)]
     if data_set.empty:
         revenue_of_total_products_bought = 0
     else:
         revenue_of_total_products_bought = get_bought_product_details(data_set)   
     profit_percent = (revenue_of_total_products_sold - revenue_of_total_products_bought)
     print("[magenta]profit_percent :[/magenta]",profit_percent)
     
     


