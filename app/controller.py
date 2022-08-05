
from functions import advance_time,buy_product, sell_product, report_inventory, report_revenue, report_profit
import sys

def services(args):
    if sys.argv[1] == "--advance-time":
        advance_time(args)
    if args.command == 'report':
        if sys.argv[2]== 'inventory':
            report_inventory(args)
        elif sys.argv[2] == 'revenue': 
            report_revenue(args)
        elif sys.argv[2] == 'profit':
            report_profit(args)
    if args.command == 'sell':
        sell_product(args)
    if args.command == 'buy':
        buy_product(args)

