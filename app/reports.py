import pandas as pd
"""to avoid SettingWithCopyWarning """
pd.options.mode.chained_assignment = None 
from config import bought_file, sold_file
from datetime import date
from rich import print
from matplotlib import pyplot as plt


"""plot for total products bought on particular date"""
dataset1 = pd.read_csv(bought_file)
#groupby buy_date and get the bought products count on particular date
dataset1['count']= dataset1.groupby(['buy_date'])['id'].transform('count')
print(dataset1)
dataset1 = dataset1.drop(['id','product_name','buy_price','expiration_date'],axis = 1).drop_duplicates()
print(dataset1)
#adding values from dataset to list
x_values = dataset1['buy_date'].to_list()
print("x_values",x_values)
y_values = dataset1['count'].to_list()
print("y_values",y_values)
plt.title("Plot for products bought on particular date")
plt.xlabel("Dates")
plt.ylabel("No of products bought")
plt.bar(x_values,y_values, color ='maroon', width = 0.2)
plt.show()

"""plot for total products sold on particular date"""
dataset2 = pd.read_csv(sold_file)
#groupby sell_date and get the sold products count on particular date
dataset2['count']= dataset2.groupby(['sell_date'])['id'].transform('count')
dataset2 = dataset2.drop(['id','bought_id'],axis = 1).drop_duplicates()
#adding values from dataset to list
x_values = dataset2['sell_date'].to_list()
y_values = dataset2['count'].to_list()
plt.title("Plot for products sold on particular date")
plt.xlabel("Dates")
plt.ylabel("No of products sold")
plt.bar(x_values,y_values, color ='maroon', width = 0.2)
plt.show()

"""plot for profit on particulate date"""
dataset3= pd.read_csv(sold_file)
dataset3 = dataset3.drop(['bought_id','id'], axis=1 )
x_values = dataset3['sell_date'].drop_duplicates().to_list()
#groupby sell_date and sell_price and get the products count 
dataset3['count']= dataset3.groupby(['sell_date','sell_price'])['sell_price'].transform('count')
dataset3 = dataset3.drop_duplicates()
y_values =[]
#iterate through x_values list(which contains dates values) to calculate revenue on particular date
for x in range(len(x_values)): 
     #consider dataset which satisfies x_values[x] date
     dataset_date = dataset3.loc[dataset3['sell_date'] == x_values[x]]
     dataset_date['revenue_per_product'] = dataset_date['sell_price']*dataset_date['count']
     revenue_dataset_date = dataset_date['revenue_per_product'].sum() 
     #adding revenue values to y_values list
     y_values.append(revenue_dataset_date)
# creating the bar plot
plt.bar(x_values, y_values, color ='maroon', width = 0.2)
plt.title("Plot for products revenue on particular date")
plt.xlabel("Dates")
plt.ylabel("products revenue")
plt.show()

