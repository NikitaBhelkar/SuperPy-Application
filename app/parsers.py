import argparse
from argparse import ArgumentParser
from datetime import datetime


def create_argparser():

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--advance-time", help="date is advanced by number of days", type=str)

    parser.add_argument("--visual-reports",help ="shows visual reports for products bought, products sold and profit on particular dates", nargs='?')

    subparsers = parser.add_subparsers(dest='command')

    buy = subparsers.add_parser('buy', help="buy command includes product_name, price, and expiration_date in format like ""2020-01-01"" for the product", description='subparser description')
    buy.add_argument('--product-name', type = str, required=True)
    buy.add_argument('--price', type=float, required=True)
    buy.add_argument("--expiration-date", type=lambda dt: datetime.strptime(dt, '%Y-%m-%d'), required=True)
    
    sell = subparsers.add_parser('sell', help="sell command includes product_name, price for the product", description='subparser description')
    sell.add_argument('--product-name',type = str, required=True)
    sell.add_argument('--price', type=float, required=True)

    report_type = subparsers.add_parser('report',help ="reports inventory details, revenue details and profit details for the product", description='subparser description')
    report_type.add_argument('report-type', type=str, nargs='+')

    report_type.add_argument('--now', action='store_true')
    report_type.add_argument('--yesterday', action='store_true')

    report_type.add_argument('--today',action='store_true')
    report_type.add_argument('--date', type=lambda dt: datetime.strptime(dt, '%Y-%m'), nargs='?')


    return parser.parse_args()
