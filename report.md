1. While writing bought product details to bought_file, the same data is copied to bought_file_copy.
This is implemented in this way to get the latest inventory details/updates everytime, as the sold products details are removed from bought_file_copy, whenever the product is sold.
bought_file contains all the details of products from the first day, this file only keeps adding the bought products.

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


2. Rich library is uesd for writing rich text (with color) to the terminal
eg - print('[magenta]OK. Data has been loaded successfully ![/magenta]')

3. Timedelta function is used to increment the date by n no of days
eg - today_date = date.today()
     td = timedelta(int(n))
     artificial_date = (today_date + td).strftime('%Y-%m-%d')

4. tabulate() is used to display the data in tabular form on terminal.
eg - print(tabulate([data_set.columns.values.tolist()] + data_set.values.tolist(), headers='firstrow', tablefmt='grid'))

5. Below functionality is used to increment id for each row while writing data in the csv file 
    results = pd.read_csv(sold_file)
    id = len(results) + 1

6. exporting dataset value to csv file 
     data = df1.loc[df1['product_name'] != sys.argv[3]]
     data.to_csv(bought_file_copy, index=False)

7. Used Matplotlib for reporting 
   used plot, scatter and bar plot for generating reports on products
